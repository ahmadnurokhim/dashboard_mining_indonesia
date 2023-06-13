import streamlit as st
import altair as alt
import pandas as pd


st.set_page_config(layout="wide")
"# Dashboard Pertambangan Non Migas di Indonesia"
"**Ahmad Nurokhim (nurokhima20@gmail.com)**"

"### Mengenai Industri Pertambangan Non Migas"
"""Dalam beberapa tahun terakhir, sektor pertambangan Indonesia mengalami perkembangan yang cukup signifikan. Indonesia sendiri adalah produsen nikel terbesar pertama dan produsen batu bara terbesar ke tiga di dunia per 2021. Maka dari itu, akan sangat menarik utnuk dapat mengeksplorasi aspek-aspek utama di industri ini seperti produksi tahunan, ekspor, dan tren tenaga kerja dari data yang tersedia. Terlebih lagi,  Memahami interkoneksi ini sangat penting bagi pembuat kebijakan, investor, dan pemangku kepentingan untuk membuat keputusan berdasarkan informasi, dan mendorong pertumbuhan yang berkelanjutan."""
"---"

met1, met2 = st.columns(2)
with met1:
    st.metric("Produksi Non Migas 5 Tahun Terakhir", "647.08 Juta Ton", "45.65%")
    df_production = pd.read_csv("Data_2/production main clean.csv", delimiter=",")
    df_production['total'] = df_production.drop(columns='gold').sum(axis=1) + (df_production['gold']/1000)
    df_production["year"] = pd.to_datetime(df_production['year'], format='%Y')
    production_chart = alt.Chart(df_production[df_production['year']> pd.to_datetime("2015", format="%Y")]).mark_line().encode(
        alt.X('year', timeUnit='yearmonth'),
        y='total',
    )
    # st.altair_chart(production_chart, use_container_width=True)
with met2:
    st.metric("Ekspor Non Migas 5 Tahun Terakhir", "594.78 Juta Ton", "26.98%")
    df_export = pd.read_csv("Data_2/export.csv", delimiter=";")
    df_export.iloc[:, 1:] = df_export.iloc[:, 1:].multiply(1000)
    df_export["year"] = pd.to_datetime(df_export['year'], format='%Y')
    export_chart = alt.Chart(df_export[df_export['year']>pd.to_datetime("2015", format="%Y")]).mark_line().encode(
        alt.X('year', timeUnit='yearmonth'),
        y='non_migas',
    )
    # st.altair_chart(export_chart, use_container_width=True)

"---"

mid1a, mid2a = st.columns(2)
with mid1a:
    
    "### Produksi Batubara: High Volume"
    "Di antara sejumlah mineral lainnya, batubara mendominasi secara instan yang dapat terlihat dari volume produksinya yang sangat tinggi dan relatif stabil naik."
    "Menariknya, dari 1996 hingga 2021, produksi batubara tahunan menunjukkan tingkat yang konsisten, dengan sedikit penurunan di tahun 2015. Hal ini menunjukkan kekokohan sektor pertambangan batu bara serta kontribusinya yang signifikan terhadap lanskap pertambangan negara."

with mid2a:
    df_production = pd.read_csv("Data_2/production main clean.csv", delimiter=",")
    df_production.iloc[:, 3:4] = df_production.iloc[:, 3:4].multiply(1/1000)
    df_production["year"] = pd.to_datetime(df_production['year'], format='%Y')
    line1a = alt.Chart(df_production).mark_line().encode(alt.X('year', timeUnit='yearmonth'), y='coal')
    st.altair_chart(line1a, use_container_width=True)

"---"

mid1b, mid2b = st.columns(2)
with mid1b:
    df_export = pd.read_csv("Data_2/export.csv", delimiter=";")
    df_export["year"] = pd.to_datetime(df_export['year'], format='%Y')
    df_export.iloc[:, 1:] = df_export.iloc[:, 1:] * 1000

    # line1b = alt.Chart(df_export).mark_line(color='red').encode(alt.X('year', timeUnit='yearmonth'), y='migas')
    # line2b = alt.Chart(df_export).mark_line().encode(alt.X('year', timeUnit='yearmonth'), y='non_migas')
    # chart_with_labels = alt.layer(line1b, line2b).configure_legend(orient='top-left')
    linea = alt.Chart(df_export).transform_fold(['non_migas', 'migas'], ['sektor', "volume ekspor"]).mark_line().encode(
        alt.X('year', timeUnit='yearmonth'),
        y='volume ekspor:Q',
        color='sektor:N'
    )
    st.altair_chart(linea, use_container_width=True)
    
with mid2b:
    "### Ekspor Pertambangan"
    "Pada data ekspor, terlihat bahwa ekspor pertambangan non migas hampir secara umum naik sejak tahun 1996 dengan puncak ekspor pada tahun 2013. Namun tidak dapat dikatakan demikian untuk ekspor migas. Ekspor migas cenderung terus menurun dari 1996 dengan titik terendah pada tahun 2019. Pada tahun 2021, proporsi ekspor nonmigas mencapai 95.7% dari total ekspor migas-nonmigas."
    df_export_pivot = df_export[df_export['year'].dt.year==2021].drop(columns=['year', 'total']).melt(var_name='sektor', value_name='volume ekspor')
    line3b = alt.Chart(df_export_pivot).mark_bar().encode(
        x=alt.X('sektor:N', axis=alt.Axis(labelAngle=0)),
        y='volume ekspor:Q',
        color=alt.Color('sektor:N'),
        
    )
    st.altair_chart(alt.layer(line3b), use_container_width=True)
    
    "Saat kita telusuri lebih lanjut, batubara kembali menarik perhatian. Volume ekspor batubara sendiri mencakup lebih dari separuh volume ekspor mineral non migas Indonesia. Hal ini menyoroti pentingnya peran batubara dalam perekonomian negara yang digerakkan oleh ekspor"

    "Paradoks Ekspor Batubara: Volume vs. Nilai"
    "Sementara ekspor batu bara menunjukkan volume yang besar, pemeriksaan lebih dekat mengungkapkan sebuah paradoks yang menarik. Meskipun volume ekspornya tinggi, nilai ekspor batubara tampak relatif tidak stabil dan rendah secara tidak proporsional dibandingkan dengan volumenya. Keganjilan ini mengundang kita untuk menyelidiki lebih jauh faktor-faktor yang mempengaruhi dinamika harga dan kekuatan pasar yang mempengaruhi nilai ekspor batubara."

    "Konsumsi Domestik: Meningkatnya Nafsu Batu Bara"
    "Saat kami mengalihkan fokus ke dalam, kami menemukan tren menarik dalam konsumsi batubara dalam negeri. Selama bertahun-tahun, Indonesia telah menyaksikan peningkatan yang stabil dalam konsumsi batubara di dalam wilayahnya sendiri. Lintasan ke atas ini mencapai puncaknya pada tahun 2021, menggarisbawahi ketergantungan negara yang semakin besar pada batu bara sebagai sumber energi vital. Temuan ini mengisyaratkan interaksi dinamis antara pembangunan ekonomi, kebutuhan energi, dan pemanfaatan sumber daya lokal."

    "Kisah Tenaga Kerja: Naik Rollercoaster"
    "Industri pertambangan tidak hanya tentang mineral dan ekspor tetapi juga mencakup kehidupan dan mata pencaharian pekerja yang tak terhitung jumlahnya. Analisis kami terhadap tenaga kerja pertambangan mengungkap kisah yang menarik. Dari tahun 2005 hingga 2021, proporsi tenaga kerja asing di sektor ini mencapai titik terendahnya pada tahun 2015. Namun, setelah itu mulai meningkat, terus meningkat hingga mencapai puncaknya pada tahun 2020. Yang mengherankan, narasi ini berubah secara tak terduga, karena proporsinya pekerja asing anjlok pada tahun 2021, mengalami penurunan drastis hingga lebih dari setengahnya. Fluktuasi yang signifikan ini menimbulkan pertanyaan tentang perubahan kebijakan, dinamika ketenagakerjaan, dan dampak keseluruhan terhadap stabilitas dan produktivitas sektor tersebut."

    "Kesimpulan:"
    "Kesimpulannya, perjalanan analisis data kami melalui industri pertambangan non-minyak dan non-gas di Indonesia telah memberikan wawasan berharga tentang aspek-aspek kunci dari sektor tersebut. Kami mengamati dominasi batubara baik dalam produksi maupun ekspor, sambil mengungkap paradoks yang menarik antara volume dan nilai. Selain itu, peningkatan konsumsi batubara domestik menunjukkan kebutuhan energi nasional yang terus meningkat. Terakhir, dinamika ketenagakerjaan menyoroti perjalanan rollercoaster yang dialami oleh pekerja asing di sektor pertambangan. Wawasan ini menawarkan sekilas ke permadani industri pertambangan Indonesia yang rumit, menyerukan eksplorasi lebih lanjut dan pemahaman yang lebih dalam tentang kekuatan pendorong dan implikasi untuk pembangunan berkelanjutan di tahun-tahun mendatang."