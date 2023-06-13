import streamlit as st
import altair as alt
import pandas as pd

def get_value_volume_2021():
    # Read the CSV files
    df_export = pd.read_csv("Data_2/export.csv", delimiter=";")
    df_coal = pd.read_csv("Data_2/coal_export.csv", delimiter=';')
    df_export_usd = pd.read_csv("Data_2/export_usd.csv", delimiter=';')
    df_coal_usd = pd.read_csv("Data_2/coal_export_usd.csv", delimiter=';')

    # Merge the DataFrames
    df_2021_ton = pd.merge(df_export[['year', 'non_migas']], df_coal[['year', 'total']], on='year')
    df_2021_usd = pd.merge(df_export_usd[['year', 'non_migas']], df_coal_usd[['year', 'total']], on='year')

    # Add a 'type' column to differentiate 'Volume' and 'Value'
    df_2021_ton['type'] = 'Volume'
    df_2021_usd['type'] = 'Value'

    # Concatenate the DataFrames
    df_2021 = pd.concat([df_2021_ton, df_2021_usd])

    # Filter for the year 2021
    df_2021 = df_2021[df_2021['year'] == 2021]

    # Multiply the relevant columns by 1000
    df_2021[['non_migas', 'total']] *= 1000
    # df_2021['non_migas'] = df_2021['non_migas'] - df_2021['total']
    df_2021['non_migas'], df_2021['total'] = df_2021['total'], df_2021['non_migas']
    df_2021.columns = ['year', 'Coal', 'Non Migas Non Coal', 'type']
    df_2021['Coal'] = df_2021['Coal']/df_2021['Non Migas Non Coal']*100
    df_2021['Non Migas Non Coal'] = 100-df_2021['Coal']
    return df_2021


st.set_page_config(layout="wide")
"# Pertambangan Non Migas di Indonesia"
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
    "Dari analisis singkat terhadap data volume produksi pertambangan non migas, batubara mendominasi secara instan di antara sejumlah mineral lainnya. Hal ini dapat terlihat dari volume produksinya yang sangat tinggi dan relatif stabil naik."
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
    # GRAFIK MIGAS NON MIGAS
    df_export = pd.read_csv("Data_2/export.csv", delimiter=";")
    df_export["year"] = pd.to_datetime(df_export['year'], format='%Y')
    df_export.iloc[:, 1:] = df_export.iloc[:, 1:] * 1000
    lineb1 = alt.Chart(df_export).transform_fold(['non_migas', 'migas'], ['sektor', "volume ekspor"]).mark_line().encode(
        alt.X('year', timeUnit='yearmonth'),
        y='volume ekspor:Q',
        color=alt.Color('sektor:N', scale=alt.Scale(scheme='dark2'))
    )
    st.altair_chart(lineb1, use_container_width=True)
    
    # GRAFIK BATUBARA NON MIGAS
    df_coal = pd.read_csv("Data_2/coal_export.csv", delimiter=';')
    df_coal["year"] = pd.to_datetime(df_export['year'], format='%Y')
    df_coal.iloc[:, 1:] = df_coal.iloc[:, 1:] * 1000
    df_export_coal = pd.merge(df_export.drop(columns=['total', 'migas']), df_coal[['year', 'total']], on='year')
    df_export_coal.columns = ['year', 'non_migas', 'batubara']
    lineb2 = alt.Chart(df_export_coal).transform_fold(['non_migas', 'batubara'], ['sektor', 'volume ekspor']).mark_line().encode(
        alt.X('year', timeUnit='yearmonth'),
        y='volume ekspor:Q',
        color=alt.Color('sektor:N', scale=alt.Scale(scheme='dark2'))
    )
    st.altair_chart(lineb2, use_container_width=True)
    
with mid2b:
    "### Ekspor Pertambangan"
    "Pada data ekspor, terlihat bahwa ekspor pertambangan non migas hampir secara umum naik sejak tahun 1996 dengan puncak ekspor pada tahun 2013. Namun tidak dapat dikatakan demikian untuk ekspor migas."
    "Ekspor migas cenderung terus menurun dari 1996 dengan titik terendah pada tahun 2019. Pada tahun 2021, proporsi ekspor nonmigas mencapai 95.7% dari total ekspor migas-nonmigas."
    df_export_pivot = df_export[df_export['year'].dt.year==2021].drop(columns=['year', 'total']).melt(var_name='sektor', value_name='volume ekspor')
    line3b = alt.Chart(df_export_pivot).mark_arc(innerRadius=50).encode(
        theta='volume ekspor:Q',
        color=alt.Color('sektor:N', scale=alt.Scale(scheme='dark2'))
        
    )
    st.altair_chart(alt.layer(line3b), use_container_width=True)

    "Apabila ditelusuri lebih lanjut, volume ekspor batubara sendiri mencakup ***58.1%*** volume ekspor mineral non migas Indonesia. Hal ini menegaskan pentingnya peran batubara dalam perekonomian negara."
'---'
mid1c, mid2c = st.columns(2)
with mid1c:
    "### Volume vs Nilai"
    "Meskipun volume ekspor batubara tergolong tinggi mencapai ***58.1%***, nilai ekspor batubara tampak relatif rendah secara proporsional dibandingkan dengan volume total ekspor non migas."
    "Yakni hanya mencakup ***12.1%*** dari total nilai ekspor non migas."
    "Hal ini dapat disebabkan oleh banyak faktor, seperti dinamika harga batubara global dan permintaan pasar."

with mid2c:
    df_2021_vv = get_value_volume_2021()
    df_2021_melt = pd.melt(df_2021_vv.drop(columns='year'), id_vars='type', var_name='sektor', value_name='percentage' )
    vol_val = alt.Chart(df_2021_melt).mark_bar().encode(
        x=alt.X('type:N', axis=alt.Axis(labelAngle=0)),
        y='percentage:Q',
        color=alt.Color('sektor:N', scale=alt.Scale(scheme='dark2')),
        order=alt.Order('sektor')
    )
    st.altair_chart(vol_val, use_container_width=True)

"---"
mid1d, mid2d = st.columns(2)

with mid1d:
    st.write()
    st.write()
    st.write()
    df_coal_prod_exp = pd.merge(df_production[['year', 'coal']], df_coal[['year','total']], on='year')
    df_coal_prod_exp.columns = ['year', 'coal production', 'coal export']
    chart = alt.Chart(df_coal_prod_exp).transform_fold(['coal production', 'coal export'], ['label', 'value (ton)']).mark_line().encode(
        x=alt.X('year', timeUnit='yearmonth'),
        y='value (ton):Q',
        color=alt.Color('label:N', scale=alt.Scale(scheme='dark2'))
    )
    st.altair_chart(chart, use_container_width=True)

with mid2d:
    "### Konsumsi Domestik Batu Bara"
    "Hal yang menarik saat menggali lebih dalam terkait ini yakni mengenai konsumsi domestik batubara."
    "Selama beberapa tahun tearkhir, volume produksi batubara relatif stabil naik hingga tahun 2021. Menariknya, hal ini tidak diikuti oleh volume ekspor batubara yang meningkat. Justru, volume ekspor batu bara cenderung stagnan di level yang sama."

    "Temuan ini dapat mengisyaratkan dua hal:"
    "- Ketergantungan negara yang semakin besar pada batubara sebagai sumber energi. Maka dari itu, diharapkan negara dapat mengupayakan lebih pada sumber energi alternatif lainnya, terutama energi bersih."
    "- Meningkatnya keamanan suplai batu bara (dan energi secara umum) dan meningkatnya perputaran ekonomi dalam negeri. Hal ini menandakan pentingnya peran batu bara dalam pembangunan ekonomi, kebutuhan energi, serta pemanfaatan sumber daya lokal."

    "Kisah Tenaga Kerja: Naik Rollercoaster"
    "Industri pertambangan tidak hanya tentang mineral dan ekspor tetapi juga mencakup kehidupan dan mata pencaharian pekerja yang tak terhitung jumlahnya. Analisis kami terhadap tenaga kerja pertambangan mengungkap kisah yang menarik. Dari tahun 2005 hingga 2021, proporsi tenaga kerja asing di sektor ini mencapai titik terendahnya pada tahun 2015. Namun, setelah itu mulai meningkat, terus meningkat hingga mencapai puncaknya pada tahun 2020. Yang mengherankan, narasi ini berubah secara tak terduga, karena proporsinya pekerja asing anjlok pada tahun 2021, mengalami penurunan drastis hingga lebih dari setengahnya. Fluktuasi yang signifikan ini menimbulkan pertanyaan tentang perubahan kebijakan, dinamika ketenagakerjaan, dan dampak keseluruhan terhadap stabilitas dan produktivitas sektor tersebut."

    "Kesimpulan:"
    "Kesimpulannya, perjalanan analisis data kami melalui industri pertambangan non-minyak dan non-gas di Indonesia telah memberikan wawasan berharga tentang aspek-aspek kunci dari sektor tersebut. Kami mengamati dominasi batubara baik dalam produksi maupun ekspor, sambil mengungkap paradoks yang menarik antara volume dan nilai. Selain itu, peningkatan konsumsi batubara domestik menunjukkan kebutuhan energi nasional yang terus meningkat. Terakhir, dinamika ketenagakerjaan menyoroti perjalanan rollercoaster yang dialami oleh pekerja asing di sektor pertambangan. Wawasan ini menawarkan sekilas ke permadani industri pertambangan Indonesia yang rumit, menyerukan eksplorasi lebih lanjut dan pemahaman yang lebih dalam tentang kekuatan pendorong dan implikasi untuk pembangunan berkelanjutan di tahun-tahun mendatang."

