import streamlit as st
from streamlit_autorefresh import st_autorefresh
import plotly.express as px
from backend import analyse
from backend.start import DB_NAME

st.set_page_config(page_title="dashboard",
                       layout="wide",
                       page_icon="misc/icon128.png")

##### sidebar

if st.sidebar.button(label="refresh", key=1):
    st.rerun()

# pages
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

page = st.sidebar.selectbox(
    "page",
    ["dashboard", "player", "bot"],
    index=["dashboard", "player", "bot"].index(st.session_state.page))

st.session_state.page = page

#fais un grand espace
for _ in range(33):
    st.sidebar.write("")

theme = st.sidebar.selectbox(
    "theme",
    ["Dark", "Light"])
if theme == "Light":
    st.sidebar.write("c'est non ")

#refresh every 10 sec if change
st_autorefresh(interval=10_000, key="datarefresh")


########################################

#page dashboard du serv
if page == "dashboard":

    st.title(f"Dashboard {DB_NAME}")

    #int
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Nombre de joueurs unique", analyse.get_total_players())
    with col2:
        st.metric("Nombre de messages", analyse.get_total_message())
    with col3:
        st.metric("uptime", analyse.get_uptime())

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Nombre de morts", analyse.get_total_deaths())
    with col2:
        st.metric("Kills par joueur", analyse.get_deaths_by_type()[0])
    with col3:
        st.metric("Kills par monstres",analyse.get_deaths_by_type()[1])
    with col4:
        st.metric("Kills par environnement", analyse.get_deaths_by_type()[2])
    with col5:
        st.metric("Moyenne de morts", analyse.get_average_deaths())

    st.divider() ##################################################################################

    col1, col2 = st.columns(2)

    #pie chart
    with col1:
        palette = ["#0F57C2", "#2171b5", "#4292c6", "#6baed6", "#9ecae1", "#c6dbef", "#EBF2F9"]

        df = analyse.get_death_distribution()

        df["type_lisible"] = df["type"].map({
            "death.attack.player": "kill par un joueur",
            "death.fell.accident.generic": "chute accidentelle",
            "death.attack.explosion.player": "explosion par un joueur (cristaux de l'end)",
            "death.fell.assist": "chute assistée",
            "death.attack.drown": "noyade",
            "death.attack.outsideBorder": "hors limites de la map",
            "death.attack.arrow": "flèche",
            "death.attack.mob": "kill par un mob",
            "death.attack.player.item": "kill par objet d’un joueur",
            "death.attack.lava": "lave"})

        fig = px.pie(
            df,
            names="type_lisible",
            values="nombre",
            title="Répartition des types de mort",
            color="type",
            width=600,
            height=600,
            labels={"nombre": "Nombre de morts"},
            color_discrete_sequence=palette)

        fig.update_traces(textinfo="value")

        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5))

        st.plotly_chart(fig, width='content')

    # top_chatters
    with col2:
        st.subheader("plus gros parleur")
        df = analyse.get_top_chatters()
        st.dataframe(df, hide_index=True, width="stretch")

    st.divider()  ##################################################################################
    #chat minecraft

    import base64


    def load_font_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()


    font_base64 = load_font_base64("misc/minecraft_font.woff2")

    st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'Minecraft';
        src: url(data:misc/minecraft_font.woff2;base64,{font_base64}) format('woff2');
    }}

    .minecraft-chat {{
        font-family: 'Minecraft', monospace;
        background-color: #1E1E1E;
        color: #E0E0E0;
        padding: 12px;
        border-radius: 6px;
        height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-size: 16px;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="minecraft-chat">[12:00] <Apollo> Test police Minecraft</div>', unsafe_allow_html=True)

    st.divider() ###################################################################################

    st.subheader(" Heartbeat ")

    heartbeat_playercount = px.line(
        analyse.get_playercount_over_time(),
        x="temps",
        y="nombre de joueurs",
        markers=False,
        title="Joueurs en ligne",
        range_y=[0, 40])

    heartbeat_message = px.line(
        analyse.get_message_over_time(),
        x="temps",
        y="message",
        markers=False,
        title="Messages par minute",
        range_y=[0, 60])

    heartbeat_ping = px.line(
        analyse.get_ping_over_time(),
        x="temps",
        y="ping",
        markers=False,
        title="Ping du bot",
        range_y=[-1, 70])

    st.plotly_chart(heartbeat_playercount, width='stretch')
    st.plotly_chart(heartbeat_message, width='stretch')
    st.plotly_chart(heartbeat_ping, width='stretch')

    st.divider() ###################################################################################

elif page == "plater":
    pass

#page pour le bot
elif page == "bot":
    st.title("comming soon ")
