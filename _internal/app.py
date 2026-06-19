import streamlit as st
import json
import os
import pandas as pd
from utils import NATURES, calculate_stat, get_type_effectiveness, calculate_speed, calculate_damage

# Set page config
st.set_page_config(page_title="Pokemon Champions Team Builder", layout="wide")

def get_data_dir():
    if os.path.isdir('data'):
        return 'data'
    return '.'

# Load data
@st.cache_data
def load_data():
    data_dir = get_data_dir()
    with open(os.path.join(data_dir, 'pokemon.json'), 'r') as f:
        pokemon = json.load(f)
    with open(os.path.join(data_dir, 'items.json'), 'r') as f:
        items = json.load(f)
    with open(os.path.join(data_dir, 'moves.json'), 'r') as f:
        moves = json.load(f)
    with open(os.path.join(data_dir, 'movepools.json'), 'r') as f:
        movepools = json.load(f)
    return pokemon, items, moves, movepools

pokemon_data, items_data, moves_data, movepools_data = load_data()

pokemon_names = [""] + [p['name'] for p in pokemon_data]
item_names = [""] + [i['name'] for i in items_data]
move_names = [""] + sorted(list(moves_data.keys()))
nature_names = list(NATURES.keys())
all_types = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
all_abilities = sorted(list(set(a for p in pokemon_data for a in p['abilities'])))

def get_pokemon_by_name(name):
    for p in pokemon_data:
        if p['name'] == name:
            return p
    return None

def get_item_by_name(name):
    for i in items_data:
        if i['name'] == name:
            return i
    return None

# Initialize session state for 6 pokemon
if 'team' not in st.session_state:
    st.session_state.team = []
    for i in range(6):
        st.session_state.team.append({
            'name': '',
            'item': '',
            'ability': '',
            'nature': 'Adamant (+Atk, -SpA)',
            'evs': {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0},
            'moves': ['', '', '', '']
        })

st.title("Pokemon Champions Doubles Team Builder")

with st.expander("Save / Load Team"):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Save Team")
        team_json = json.dumps(st.session_state.team, indent=4)
        st.download_button("Download Team (JSON)", data=team_json, file_name="my_team.json", mime="application/json")
    with col2:
        st.subheader("Load Team")
        uploaded_file = st.file_uploader("Upload Team (JSON)", type="json")
        if uploaded_file is not None:
            try:
                loaded_team = json.load(uploaded_file)
                if len(loaded_team) == 6:
                    # Update session state
                    st.session_state.team = loaded_team
                    st.success("Team loaded successfully!")
                    st.button("Apply / Refresh", on_click=lambda: None)
                else:
                    st.error("Invalid team format.")
            except Exception as e:
                st.error(f"Error loading team: {e}")

tabs = st.tabs(["Team Builder", "Defensive Coverage", "Offensive Coverage", "Speed Tiers", "Damage Calculator"])

with tabs[0]:
    st.header("Team Builder")
    
    with st.expander("Filter Pokemon Search"):
        f_cols = st.columns(3)
        filter_type = f_cols[0].selectbox("Filter by Type", ["Any"] + all_types)
        filter_ability = f_cols[1].selectbox("Filter by Ability", ["Any"] + all_abilities)
        filter_moves = f_cols[2].multiselect("Filter by Moves Learned", move_names[1:])
        filter_moves_op = st.radio("Move Filter Logic", ["AND", "OR"], horizontal=True)
        
    filtered_pokemon_names = [""]
    for p in pokemon_data:
        if filter_type != "Any" and filter_type.lower() not in [t.lower() for t in p['types']]:
            continue
        if filter_ability != "Any" and filter_ability not in p['abilities']:
            continue
        if filter_moves:
            base_name = p['name'].split(' (')[0].replace('Mega ', '').replace('Alolan ', '').replace('Galarian ', '').replace('Hisuian ', '').replace('Paldean ', '').replace('Blade ', '')
            if base_name.endswith(' X') or base_name.endswith(' Y'):
                base_name = base_name[:-2]
            p_moves = movepools_data.get(base_name, [])
            if filter_moves_op == "AND":
                if not all(m in p_moves for m in filter_moves): continue
            else:
                if not any(m in p_moves for m in filter_moves): continue
        filtered_pokemon_names.append(p['name'])

    cols = st.columns(3)
    
    for i in range(6):
        col = cols[i % 3]
        with col:
            st.subheader(f"Slot {i+1}")
            current_p = st.session_state.team[i]['name']
            options = filtered_pokemon_names if current_p in filtered_pokemon_names else filtered_pokemon_names + [current_p]
            p_name = st.selectbox("Pokemon", options, key=f"p_name_{i}", index=options.index(current_p) if current_p in options else 0)
            
            if p_name:
                p_info = get_pokemon_by_name(p_name)
                st.session_state.team[i]['name'] = p_name
                
                # Display image
                if p_info.get('image'):
                    st.image(p_info['image'], width=100)
                
                st.write(f"**Types:** {', '.join([t.title() for t in p_info['types']])}")
                
                # Update ability options based on selected pokemon
                abilities = p_info['abilities']
                current_ability = st.session_state.team[i]['ability']
                ab_index = abilities.index(current_ability) if current_ability in abilities else 0
                st.session_state.team[i]['ability'] = st.selectbox("Ability", abilities, key=f"ab_{i}", index=ab_index)
                
                # Item
                current_item = st.session_state.team[i]['item']
                it_index = item_names.index(current_item) if current_item in item_names else 0
                selected_item = st.selectbox("Item", item_names, key=f"it_{i}", index=it_index)
                st.session_state.team[i]['item'] = selected_item
                item_info = get_item_by_name(selected_item)
                if item_info and item_info.get('image'):
                    st.image(item_info['image'], width=30)
                
                # Nature
                current_nature = st.session_state.team[i]['nature']
                nat_index = nature_names.index(current_nature) if current_nature in nature_names else 0
                st.session_state.team[i]['nature'] = st.selectbox("Nature", nature_names, key=f"nat_{i}", index=nat_index)
                
                # SPs
                sp_keys = ['hp', 'atk', 'def', 'spa', 'spd', 'spe']
                current_sps = {k: st.session_state.get(f"sp_{i}_{k}", st.session_state.team[i]['evs'][k]) for k in sp_keys}
                used_sps = sum(current_sps.values())
                
                if used_sps > 66:
                    st.warning("Max 66 SPs allowed! Please reduce some values.")
                
                st.write(f"**SPs (Used: {used_sps} / 66)**")
                sp_cols = st.columns(6)
                for j, stat in enumerate(sp_keys):
                    remaining = 66 - used_sps + current_sps[stat]
                    dynamic_max = min(32, max(0, remaining))
                    val = min(current_sps[stat], dynamic_max)
                    st.session_state.team[i]['evs'][stat] = sp_cols[j].number_input(stat.upper(), min_value=0, max_value=int(dynamic_max), value=int(val), key=f"sp_{i}_{stat}")
                
                # Calculated Stats
                stats_str = []
                for stat in sp_keys:
                    base = p_info['stats'][stat]
                    sp = st.session_state.team[i]['evs'][stat]
                    nature = st.session_state.team[i]['nature']
                    calc = calculate_stat(base, sp, nature, stat)
                    stats_str.append(f"{stat.upper()}: {calc}")
                st.caption("Stats: " + " | ".join(stats_str))
                
                # Moves
                for m in range(4):
                    current_move = st.session_state.team[i]['moves'][m]
                    mv_index = move_names.index(current_move) if current_move in move_names else 0
                    st.session_state.team[i]['moves'][m] = st.selectbox(f"Move {m+1}", move_names, key=f"mv_{i}_{m}", index=mv_index)
            else:
                st.session_state.team[i]['name'] = ''

with tabs[1]:
    st.header("Defensive Coverage")
    st.write("Weaknesses and Resistances for each type against your team.")
    
    types = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
    
    def_data = []
    for t in types:
        row = {"Attack Type": t}
        for i, p in enumerate(st.session_state.team):
            if p['name']:
                p_info = get_pokemon_by_name(p['name'])
                eff = get_type_effectiveness(t, p_info['types'])
                row[p['name']] = eff
        def_data.append(row)
        
    if any(p['name'] for p in st.session_state.team):
        df_def = pd.DataFrame(def_data)
        st.dataframe(df_def.style.map(lambda x: "background-color: #ff9999" if x > 1 else ("background-color: #99ff99" if isinstance(x, (int, float)) and x < 1 else ""), subset=[p['name'] for p in st.session_state.team if p['name']]))
    else:
        st.info("Add Pokemon to your team to see coverage.")

with tabs[2]:
    st.header("Offensive Coverage")
    st.write("See how your team hits all pokemon by default, or filter by a specific target.")
    
    target_name = st.selectbox("Target Pokemon", ["All"] + pokemon_names[1:], key="target_off")
    targets = [get_pokemon_by_name(target_name)] if target_name != "All" else pokemon_data
    
    off_data = []
    for target_info in targets:
        bst = sum(target_info['stats'].values())
        best_eff = -1
        best_move = ""
        best_attacker = ""
        coverage_count = 0
        
        for p in st.session_state.team:
            if p['name']:
                p_has_coverage = False
                for m in p['moves']:
                    if m:
                        move_info = moves_data[m]
                        m_type = move_info['type']
                        if m_type != "Unknown":
                            eff = get_type_effectiveness(m_type, target_info['types'])
                            if eff > 1:
                                p_has_coverage = True
                            if eff > best_eff:
                                best_eff = eff
                                best_move = m
                                best_attacker = p['name']
                if p_has_coverage:
                    coverage_count += 1
                                
        if best_eff != -1:
            off_data.append({
                "Target Pokemon": target_info['name'],
                "Coverage Count": coverage_count,
                "Max Effectiveness": best_eff,
                "Best Move": best_move,
                "Attacker": best_attacker,
                "BST": bst
            })
            
    if off_data:
        df_off = pd.DataFrame(off_data).sort_values(by=["BST", "Coverage Count", "Max Effectiveness"], ascending=[False, False, False]).drop(columns=["BST"])
        st.dataframe(df_off.style.map(lambda x: "background-color: #99ff99" if x > 1 else ("background-color: #ff9999" if isinstance(x, (int, float)) and x < 1 else ""), subset=["Max Effectiveness"]))
    else:
        st.info("Add moves to your team to see offensive coverage.")

with tabs[3]:
    st.header("Speed Tiers")
    col1, col2, col3 = st.columns(3)
    tailwind = col1.checkbox("Tailwind")
    trick_room = col2.checkbox("Trick Room")
    
    st.write("Weather / Conditions")
    weather_speed = st.radio("Weather", ["None", "Sun", "Rain", "Sand", "Snow"], horizontal=True, key="weather_speed")
    
    st.subheader("Speed Tiers")
    
    stages_dict = {}
    team_has_pokemon = any(p['name'] for p in st.session_state.team)
    if team_has_pokemon:
        st.write("Adjust stages for your team:")
        stage_cols = st.columns(6)
        for i, p in enumerate(st.session_state.team):
            if p['name']:
                stages_dict[i] = stage_cols[i].number_input(f"{p['name'][:10]} Stages", min_value=-6, max_value=6, value=0, key=f"spe_stage_{i}")
                
    speed_data = []
    import math
    # Add all pokemon default speeds
    for p in pokemon_data:
        base_spe = p['stats']['spe']
        max_spe = calculate_stat(base_spe, 32, 'Timid', 'spe')
        
        # Weather ability check for all pokemon
        abilities = p['abilities']
        ability_mult = 1.0
        if weather_speed == "Sun" and "Chlorophyll" in abilities:
            ability_mult = 2.0
        elif weather_speed == "Rain" and "Swift Swim" in abilities:
            ability_mult = 2.0
        elif weather_speed == "Sand" and "Sand Rush" in abilities:
            ability_mult = 2.0
        elif weather_speed == "Snow" and "Slush Rush" in abilities:
            ability_mult = 2.0
            
        calc_spe = math.floor(max_spe * ability_mult)
        final_spe = calculate_speed(calc_spe, 0, False, trick_room)
        
        bst = sum(p['stats'].values())
        speed_data.append({
            "Pokemon": p['name'],
            "Speed": final_spe,
            "Type": "All Pokemon (Max Speed)",
            "BST": bst
        })
        
    # Add team speeds
    for i, p in enumerate(st.session_state.team):
        if p['name']:
            p_info = get_pokemon_by_name(p['name'])
            base_spe = p_info['stats']['spe']
            calc_spe = calculate_stat(base_spe, p['evs']['spe'], p['nature'], 'spe')
            
            # Weather ability check for equipped ability
            ability = p['ability']
            ability_mult = 1.0
            if weather_speed == "Sun" and ability == "Chlorophyll":
                ability_mult = 2.0
            elif weather_speed == "Rain" and ability == "Swift Swim":
                ability_mult = 2.0
            elif weather_speed == "Sand" and ability == "Sand Rush":
                ability_mult = 2.0
            elif weather_speed == "Snow" and ability == "Slush Rush":
                ability_mult = 2.0
                
            calc_spe = math.floor(calc_spe * ability_mult)
            
            stages = stages_dict.get(i, 0)
            final_spe = calculate_speed(calc_spe, stages, tailwind, trick_room)
            bst = sum(p_info['stats'].values())
            speed_data.append({
                "Pokemon": f"{p['name']} (Your Team Slot {i+1})",
                "Speed": final_spe,
                "Type": "Your Team",
                "BST": bst
            })
            
    df_speed = pd.DataFrame(speed_data)
    df_speed = df_speed.sort_values(by=["Speed", "BST"], ascending=[trick_room, False])
    st.dataframe(df_speed.style.map(lambda x: "background-color: #add8e6" if x == "Your Team" else "", subset=["Type"]))

with tabs[4]:
    st.header("Damage Calculator")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Attacker")
        atk_p = st.selectbox("Attacker (from team)", [p['name'] for p in st.session_state.team if p['name']])
        if atk_p:
            atk_team_idx = [p['name'] for p in st.session_state.team].index(atk_p)
            atk_info = st.session_state.team[atk_team_idx]
            atk_base = get_pokemon_by_name(atk_p)
            if atk_base.get('image'):
                st.image(atk_base['image'], width=100)
            atk_move = st.selectbox("Move", [m for m in atk_info['moves'] if m])
            
            helping_hand = st.checkbox("Helping Hand (+50%)")
            
    with c2:
        st.subheader("Defender")
        def_p = st.selectbox("Defender", pokemon_names, key="def_calc")
        if def_p:
            def_base = get_pokemon_by_name(def_p)
            if def_base.get('image'):
                st.image(def_base['image'], width=100)
            
            friend_guard = st.checkbox("Friend Guard (-25%)")
            reflect = st.checkbox("Reflect / Light Screen (-50% in singles, -33% in doubles - assuming doubles here)")
            
    weather = st.selectbox("Weather", ["None", "Sun", "Rain", "Sand", "Snow"])
    terrain = st.selectbox("Terrain", ["None", "Electric", "Grassy", "Misty", "Psychic"])
    
    if atk_p and def_p and atk_move:
        m_info = moves_data[atk_move]
        if m_info['power']:
            power = m_info['power']
            
            # calculate attacker stat
            cat = m_info['category']
            stat_name = 'atk' if cat == 'Physical' else 'spa'
            a_stat = calculate_stat(atk_base['stats'][stat_name], atk_info['evs'][stat_name], atk_info['nature'], stat_name)
            
            # calculate defender stat (assuming max HP / max Def/SpD for worst case, or just base 0 EVs)
            # Let's assume 0 EVs, neutral nature for defender
            d_stat_name = 'def' if cat == 'Physical' else 'spd'
            d_stat = calculate_stat(def_base['stats'][d_stat_name], 0, 'Neutral', d_stat_name)
            
            modifiers = []
            if helping_hand: modifiers.append(1.5)
            if friend_guard: modifiers.append(0.75)
            if reflect: modifiers.append(0.66) # doubles screen modifier
            
            eff = get_type_effectiveness(m_info['type'], def_base['types'])
            modifiers.append(eff)
            
            # STAB
            if m_info['type'].lower() in [t.lower() for t in atk_base['types']]:
                modifiers.append(1.5)
                
            damage = calculate_damage(50, power, a_stat, d_stat, modifiers)
            
            # Defender HP
            d_hp = calculate_stat(def_base['stats']['hp'], 0, 'Neutral', 'hp')
            pct = (damage / d_hp) * 100
            
            st.success(f"**Damage:** {damage} ({pct:.1f}% of {d_hp} HP) - {eff}x Effectiveness")
        else:
            st.warning("Selected move does not have a base power (status move).")

# --- UPDATE BUTTON ---
st.markdown(
    """
    <style>
    button[kind="primary"] {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 9999 !important;
        padding: 0.25rem 0.5rem !important;
        font-size: 12px !important;
        min-height: 30px !important;
        width: auto !important;
        background-color: #d3d3d3 !important;
        color: black !important;
        border: 1px solid #d3d3d3 !important;
        transition: all 0.2s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: black !important;
        color: white !important;
        border: 1px solid black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("🔄 Update App", type="primary"):
    with st.spinner("Downloading updates from GitHub..."):
        try:
            import urllib.request
            import zipfile
            import io
            import shutil
            import os
            import sys
            
            url = "https://github.com/zhamilt98/champTB/archive/refs/heads/main.zip"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with zipfile.ZipFile(io.BytesIO(response.read())) as z:
                    root_dir = z.namelist()[0]
                    has_src = any(name.startswith(f"{root_dir}src/") for name in z.namelist())
                    
                    is_exe = hasattr(sys, '_MEIPASS')
                    project_root = os.getcwd()
                    
                    for file_info in z.infolist():
                        if file_info.is_dir(): continue
                        rel_path = file_info.filename[len(root_dir):]
                        
                        if is_exe:
                            filename = os.path.basename(rel_path)
                            if filename.endswith('.py') or filename.endswith('.json'):
                                target_path = os.path.join(project_root, filename)
                            else:
                                continue
                        else:
                            if not has_src:
                                if rel_path.endswith('.json'):
                                    target_path = os.path.join(project_root, 'data' if os.path.isdir('data') else '.', rel_path)
                                else:
                                    continue
                            else:
                                target_path = os.path.join(project_root, rel_path)
                                
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        try:
                            with z.open(file_info) as source, open(target_path, "wb") as target:
                                shutil.copyfileobj(source, target)
                        except PermissionError:
                            pass
            st.cache_data.clear()
            st.success("Update successful! If the app doesn't reload automatically, please restart it.")
        except Exception as e:
            st.error(f"Update failed: {e}")
