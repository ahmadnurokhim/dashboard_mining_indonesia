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
"""Dalam beberapa tahun terakhir, sektor pertambangan Indonesia mengalami perkembangan yang cukup signifikan. Indonesia sendiri adalah produsen nikel terbesar pertama dan produsen batu bara terbesar ke tiga di dunia per 2021. Maka dari itu, akan sangat menarik untuk dapat mengeksplorasi aspek-aspek utama di industri ini seperti produksi tahunan, ekspor, dan tren tenaga kerja dari data yang tersedia. Terlebih lagi,  Memahami interkoneksi ini sangat penting bagi pembuat kebijakan, investor, dan pemangku kepentingan untuk membuat keputusan berdasarkan informasi, dan mendorong pertumbuhan yang berkelanjutan."""
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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Produksi Non Migas', 'Ekspor Pertambangan', 'Volume vs Nilai', 'Konsumsi Domestik Batubara', 'Tenaga Kerja Tambang', 'Kesimpulan'])
with tab1:
    col_a1, col_a2 = st.columns([2,3])
    with col_a1:
        
        "## Produksi Batubara: High Volume"
        "Dari analisis singkat terhadap data volume produksi pertambangan non migas, batubara mendominasi secara instan di antara sejumlah mineral lainnya. Hal ini dapat terlihat dari volume produksinya yang sangat tinggi dan relatif stabil naik."
        "Menariknya, dari 1996 hingga 2021, produksi batubara tahunan menunjukkan tingkat yang konsisten, dengan sedikit penurunan di tahun 2015. Hal ini menunjukkan kekokohan sektor pertambangan batu bara serta kontribusinya yang signifikan terhadap lanskap pertambangan negara."

    with col_a2:
        options = st.multiselect('Mineral Non Migas', ['coal', 'bauxite', 'gold', 'iron_sand', 'tin_concentrate',
       'copper_concentrate'], default='coal')
        df_production = pd.read_csv("Data_2/production main clean.csv", delimiter=",")
        # df_production.iloc[:, 3:4] = df_production.iloc[:, 3:4].multiply(1/1000)
        df_production['gold'] /= 1000
        df_production["year"] = pd.to_datetime(df_production['year'], format='%Y')
        df_production_to_be_charted = pd.concat([df_production[['year']], df_production[options]], axis=1)
        line1a = alt.Chart(df_production_to_be_charted).transform_fold(options, ['Mineral', 'Volume (Ton)']).mark_line().encode(
            alt.X('year', timeUnit='yearmonth'),
            y='Volume (Ton):Q',
            color=alt.Color('Mineral:N', scale=alt.Scale(scheme='dark2'))
        )
        st.altair_chart(line1a, use_container_width=True)
        
with tab2:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
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
    "---"
    with col_b2:
        "## Tren Ekspor Pertambangan"
        "Pada data ekspor, terlihat bahwa ekspor pertambangan non migas hampir secara umum naik sejak tahun 1996 dengan puncak ekspor pada tahun 2013. Namun tidak dapat dikatakan demikian untuk ekspor migas."
        "Ekspor migas cenderung terus menurun dari 1996 dengan titik terendah pada tahun 2019. Pada tahun 2021, proporsi ekspor nonmigas mencapai 95.7% dari total ekspor migas-nonmigas."
        df_export_pivot = df_export[df_export['year'].dt.year==2021].drop(columns=['year', 'total']).melt(var_name='sektor', value_name='volume ekspor')
        line3b = alt.Chart(df_export_pivot).mark_arc(innerRadius=50).encode(
            theta='volume ekspor:Q',
            color=alt.Color('sektor:N', scale=alt.Scale(scheme='dark2'))
            
        )
        st.altair_chart(alt.layer(line3b), use_container_width=True)

        "Apabila ditelusuri lebih lanjut, volume ekspor batubara sendiri mencakup ***58.1%*** volume ekspor mineral non migas Indonesia. Hal ini menegaskan pentingnya peran batubara dalam perekonomian negara."

with tab3:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        "## Volume vs Nilai"
        
        mid1c1, mid1c2, mid1c3 = st.columns([2,1,2])
        with mid1c1:
            st.metric("Rasio Volume Ekpor Batubara", "58.1%")
        with mid1c2:
            "## VS"
        with mid1c3:
            st.metric("Rasio Nilai Ekspor Batubara", "12.1%")

        "Meskipun volume ekspor batubara tergolong tinggi mencapai ***58.1%***, nilai ekspor batubara tampak relatif rendah secara proporsional dibandingkan dengan volume total ekspor non migas."
        "Yakni hanya mencakup ***12.1%*** dari total nilai ekspor non migas."
        "Hal ini dapat disebabkan oleh banyak faktor, seperti dinamika harga batubara global dan permintaan pasar."
        

    with col_c2:
        df_2021_vv = get_value_volume_2021()
        df_2021_melt = pd.melt(df_2021_vv.drop(columns='year'), id_vars='type', var_name='sektor', value_name='percentage' )
        vol_val = alt.Chart(df_2021_melt).mark_bar().encode(
            x=alt.X('type:N', axis=alt.Axis(labelAngle=0)),
            y='percentage:Q',
            color=alt.Color('sektor:N', scale=alt.Scale(scheme='dark2')),
            order=alt.Order('sektor')
        )
        st.altair_chart(vol_val, use_container_width=True)

with tab4:
    col_d1, col_d2 = st.columns(2)
    with col_d1:
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
        "#### Persentasi Konsumsi Domestik Batubara"
        mid1d1, mid1d2, mid1d3 = st.columns([2,1.5,2])
        with mid1d1:
            st.metric("Tahun 2012", "25.5%")
        with mid1d2:
            "## VS"
        with mid1d3:
            st.metric("Tahun 2021", "43.7%", "18.2%")

    with col_d2:
        "## Konsumsi Domestik Batu Bara"
        "Hal yang menarik saat menggali lebih dalam terkait ini yakni mengenai konsumsi domestik batubara."
        "Selama beberapa tahun tearkhir, volume produksi batubara relatif stabil naik hingga tahun 2021. Menariknya, hal ini tidak diikuti oleh volume ekspor batubara yang meningkat. Justru, volume ekspor batu bara cenderung stagnan di level yang sama."

        "Temuan ini dapat mengisyaratkan dua hal:"
        "- Ketergantungan negara yang semakin besar pada batubara sebagai sumber energi. Hal ini didukung oleh data lain yang menyebutkan bahwa pada tahun 2021, batubara menyumbang ***49.8%*** dari total kapasitas listrik PLN. Maka dari itu, diharapkan negara dapat mengupayakan lebih pada sumber energi alternatif lainnya, terutama energi bersih."
        "- Meningkatnya keamanan suplai batu bara (dan energi secara umum) dan meningkatnya perputaran ekonomi dalam negeri. Hal ini menandakan pentingnya peran batu bara dalam pembangunan ekonomi, kebutuhan energi, serta pemanfaatan sumber daya lokal."

with tab5:
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        "## Dinamika Tenaga Kerja Tambang"
        "Industri pertambangan tidak hanya tentang mineral dan ekspor tetapi juga mencakup kehidupan dan mata pencaharian pekerja yang tak terhitung jumlahnya."
        "Dari hasil pengamatan data pekerja pada pertambangan non migas, terdapat beberapa hal menarik:"
        """- Dilihat secara keseluruhan, terdapat gelombang jumlah pekerja WNI pada tahun 2010-2018 dengan puncak jumlah pekerja pada tahun 2014.
    - Jumlah pekerja SLTA kebawah selalu mendominasi, namun dengan proporsi yang semakin menurun. Hal ini berarti, secara rata-rata, tingkat pendidikan pekerja pertambangan non migas semakin meningkat.
    - Proporsi pekerja WNA relatif tinggi di awal, lalu turun dengan titik terendah di tahun 2015 dan naik kembali hingga 2020. Namun 2021, proporsi pekerja WNA anjlok ke ***0.99%*** dari total pekerja."""
        "Beberapa tahun terakhir, terkadang muncul isu terkait pekerja asing yang mulai banyak masuk ke berbagai industri di Indonesia, tak terlepas sektor pertambangan. Terlihat dari data bahwa memang benar persentase pekerja WNA meningkat hingga 2020. Hal ini dipengaruhi oleh dua faktor yakni:"
        """- Meningkatnya jumlah pekerja WNA
    - Menurunnya jumlah pekerja WNI"""
        "Namun perlu diingat bahwa persentase ini berubah berubah drastis pada tahun 2021, yang kemungkinan besar dipengaruhi oleh COVID-19."

    with col_e2:
        tab_e1, tab_e2 = st.tabs(['Tingkat Pendidikan Pekerja', 'Proporsi Pekerja WNA'])
        with tab_e1:
            df_workers = pd.read_csv("Data_2/workers main clean.csv", delimiter=",")
            df_workers['year'] = pd.to_datetime(df_workers['year'], format='%Y')
            df_workers.rename(columns={'post_graduate': 'Pasca Sarjana', 'diploma_graduate': "Diploma/Sarjana", 'senior_high_school_lower': 'SLTA kebawah'}, inplace=True)
            chart = alt.Chart(df_workers).transform_fold(
                ['Pasca Sarjana', 'Diploma/Sarjana', 'SLTA kebawah'], ['Tingkat Pendidikan', 'count']
            ).mark_line().encode(
                x=alt.X('year', timeUnit='yearmonth'),
                y='count:Q',
                color=alt.Color('Tingkat Pendidikan:N', scale=alt.Scale(scheme='dark2'))
            )
            st.altair_chart(chart, use_container_width=True)
        with tab_e2:
            chart = alt.Chart(df_workers).mark_line().encode(
                x=alt.X('year', timeUnit='yearmonth'),
                y='exp_proportion:Q',
                color=alt.Color(scale=alt.Scale(scheme='dark2'))
            )
            st.altair_chart(chart, use_container_width=True)
        
        "#### Persentasi Pekerja Diploma/Sarjana/Pasca Sarjana"
        mid1e1, mid1e2, mid1e3 = st.columns([2,1.5,2])
        with mid1e1:
            st.metric("Tahun 2005", "13.4%")
        with mid1e2:
            "## VS"
        with mid1e3:
            st.metric("Tahun 2021", "31.8%", "18.4%")
with tab6:
    "## Kesimpulan"
    "Dari hasil eksplorasi dan analisis data mengenai pertambangan non migas di Indonesia, dapat ditarik sejumlah kesimpulan yakni:"
    "- Volume produksi pertambangan non migas didominasi oleh batubara. Batubara memiliki volume produksi yang tinggi dan relatif stabil naik dalam 25 tahun terakhir, menunjukkan kekokohan sektor pertambangan batu bara di Indonesia."
    "- Ekspor pertambangan non migas cenderung meningkat, sedangkan ekspor migas cenderung terus menurun."
    "- Meskipun ekspor batubara menyumbang 58.1% dari total ekspor non migas, nilai ekspor batubara relatif rendah dengan hanya menyumbang 12.1% dari total nilai ekspor non migas."
    "- Konsumsi domestik batu bara cenderung meningkat, menunjukkan perputaran ekonomi negara yang semakin baik, namun juga menunjukkan ketergantungan yang meningkat pula terhadap batubara sebagai sumber energi. Hal ini didukung oleh data lain yang menyebutkan bahwa batubara mencakup 49.8% dari total kapasitas listrik PLN. Perlu adanya peningkatan diversivikasi sumber energi, terutama kepada alternatif energi yang lebih bersih."
    "- Tingkat pendidikan rata-rata pekerja sektor pertambangan non migas cenderung meningkat dengan pekerja sarjana/diploma/pasca sarjana memiliki proporsi 13.4% pada 2005, menjadi 31.8% pada 2021."
    "Secara keseluruhan, industri pertambangan non migas di Indonesia, terutama sektor batu bara, memiliki peran penting dalam perekonomian negara, namun industri ini juga memberikan tantangan dan peluang tersendiri yang perlu diperhatikan dalam menjaga pertumbuhan ekonomi dan diversifikasi sumber energi."
'---'