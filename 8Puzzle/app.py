import streamlit
import puzzle as pz

page=streamlit.sidebar.selectbox("Chọn cách tính Heuristic:",["h1 Distance","h2 Distance"],index=0)    
if page=="h1 Distance":
    mode=1
if page=="h2 Distance":
    mode=0


run=streamlit.sidebar.button("-------------RUN------------", use_container_width=True)


def print_path_streamlit(path, visited_states):
    if path is None:
        streamlit.error("Không tìm được lời giải!")
        return
    
    streamlit.success(f"✅ Đã tìm thấy lời giải với {len(path) - 1} bước")
    streamlit.write(f"**Tổng số trạng thái đã duyệt qua:** {len(visited_states)}")
    streamlit.write("---")
    
    # Display solution path
    streamlit.subheader("Đường đi giải pháp:")
    
    for step, (state, f, g, h) in enumerate(path):
        with streamlit.expander(f"Bước {step}: f(n)={f}, g(n)={g}, h(n)={h}", expanded=True):
            # Create clean matrix display without headers
            matrix_str = '\n'.join([' '.join([f'{cell:2}' for cell in row]) for row in state])
            streamlit.code(matrix_str, language=None)
            
            # Add step info
            if step == 0:
                streamlit.caption("Trạng thái ban đầu")
            elif step == len(path) - 1:
                streamlit.caption("Trạng thái đích")
            else:
                streamlit.caption(f"Bước di chuyển #{step}")
# Main data display area
with streamlit.container():
    streamlit.markdown('<div class="data-frame">', unsafe_allow_html=True)
    
    if run:
        col1, col2 = streamlit.columns(2)
        
        with col1:
            streamlit.write("**Trạng thái ban đầu:**")
            initial_matrix = '\n'.join([' '.join([f'{cell:2}' for cell in row]) for row in pz.initial_state])
            streamlit.code(initial_matrix, language=None)
            
        with col2:
            streamlit.write("**Trạng thái đích:**")
            goal_matrix = '\n'.join([' '.join([f'{cell:2}' for cell in row]) for row in pz.destination_state])
            streamlit.code(goal_matrix, language=None)

        path,visited_state=pz.a_star(pz.initial_state,mode)
        streamlit.subheader("🔍 Kết Quả Thuật Toán")
        print_path_streamlit(path,visited_state)
        # Create columns for organized display
        streamlit.write("---")
        streamlit.subheader("Xem các trạng thái đã duyệt qua")
        streamlit.write("---")
        with streamlit.expander(f"Đã duyệt qua {len(visited_state)} trạng thái"):
            for i,(viewed_state,f,g,h) in enumerate(visited_state):
                for row in viewed_state:
                    matrix = '\n'.join([' '.join([f'{cell:2}' for cell in row]) for row in viewed_state])
                    streamlit.write(f"f(n)={f} , g(n)={g} , h(n)={h}")
                    streamlit.code(matrix, language=None)
    else:
        streamlit.info("Nhấn nút RUN để bắt đầu thuật toán")
    
    streamlit.markdown('</div>', unsafe_allow_html=True)
