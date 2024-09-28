"""
    CURSO LENGUAJES Y SISTEMAS OPERATIVOS DE APLICACIÓN ESPACIAL
                    TRABAJO PRÁCTICO FINAL "PYTHON"
                    PROFESOR:   PABLO SOLIGO
                    ALUMNO:     DIEGO RUBÉN SANZ

    PARTE 1:
        UN SATÉLITE ARTIFICIAL CIENTÍFICO ENVÍA ENTRE SUS DATOS DE TELEMETRÍA (VALORES DE SENSORES)
        EL VALOR MEDIO DE VOLTAJE CON EL QUE ESTÁ TRABAJADO EN UN RANGO DE TIEMPO DETERMINADO (SUBSISTEMA DE POTENCIA, PCS).
        EL OBJETIVO DEL EJERCICIO ES OBTENER ESOS VALORES MEDIOS DE VOLTAJE AISLARLOS Y GRAFICARLOS.

        EL ARCHIVO BINARIO ADJUNTO (*.bin) CONTIENE TELEMETRÍA DEL SATÉLITE EN REGISTROS DE 4000 BYTES PARA UN PERÍODO DE TIEMPO.

    PARA TENER EN CUENTA:
        EL ARCHIVO CONTIENE UNA CANTIDAD DESCONOCIDA DE REGISTROS, CADA REGISTRO CONTIENE 4000 BYTES,
        CONTROLE QUE LA CANTIDAD DE BYTES DEL ARCHIVO DIVIDIDO 4000 DE RESTO 0. CASO CONTRARIO ABORTE EL PROCESO.

        EL VALOR DE VOLTAJE ESTÁ EN FORMATO "CRUDO/RAW", ES UN VALOR ENTERO ENTREGADO POR EL SENSOR AL QUE SE LE DEBE APLICAR 
        UN CÁLCULO PARA OBTENER EL VALOR DE INGENIERÍA FINAL (FLOTANTE): (raw*0.01873128+(-38.682956))

        EL VALOR DE VOLTAJE BUSCADO ESTÁ (EN FORMATO CRUDO/RAW) EN LOS BYTES 2354/2355
        (OBTENIDO DE LA SUMA DE 1604+750, 1604 DONDE COMIENZA LA TELEMETRÍA DEL SUBSISTEMA DE POTENCIA Y 
        750 LA POSICIÓN DE LA VARIABLE BUSCADA SEGÚN DOCUMENTACIÓN DEL FABRICANTE).

        NO ES CONOCIDO EL ENCODING (LITTLE-ENDIAN O BIG-ENDIAN). ¿QUÉ ENCODING TIENE SU HARDWARE?
        EN CASO DE NO SER COMPATIBLE DEBE RESOLVER EL PROBLEMA.

        PARA SU CONTROL LOS VALORES OBTENIDOS DEBEN SER APROXIMADAMENTE 33v CON BAJADAS ENTRE 31.5v y 32v (PERÍODOS DE ECLIPSE).
        GRAFIQUE CON HERRAMIENTO DE SU PREFERENCIA PARA VERIFICAR EL COMPORTAMIENTO.

    PARTE 2:
        UTILIZANDO LA INFORMACIÓN ENTREGADA POR EL FABRICANTE OBTENGA LA ÉPOCA DE LAS MEDICIONES Y
        GRAFIQUE JUNTO CON LAS MEDICIONES DE VOLTAJES.

    PARTE 3:
        SE VALORARÁ ESPECIALMENTE CUALQUIER SOLUCIÓN OFREZCA GENERICIDAD, MANTENIBILIDAD O REUSABILIDAD DE CÓDIGO.
        UTILICE LOS CONCEPTOS APRENDIDOS DE PROGRAMACIÓN ORIENTADA A OBJETOS, FUNCIONES COMO PARÁMETROS, REFLEXIÓN DE SOFTWARE,
        PARÁMETROS VARIABLES O DICCIONARIOS PARA PENSAR UNA PROPUESTA SUPERADORA.
"""

import os
import struct
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# def part1():

#     file_path_input="CGSS_20150603_091700_10020150603085920_SACD_HKTMST.bin"
#     file_size=os.path.getsize(file_path_input)
#     telemetry_package_size=4000 # Bytes

#     rest=file_size%telemetry_package_size
#     print(f"FILE SIZE: {file_size}")
#     print(f"TELEMETRY PACKAGE SIZE: {telemetry_package_size}")
#     print(f"REST PACKAGES: {rest}")
    
#     if not rest:

#         packages=file_size/telemetry_package_size
#         print(f"PACKAGES: {packages}")

#         pf=open(file_path_input,"rb")

#         file_path_output="vBatAverage_Engineering_Values.csv"
#         pfvBatAverage=open(file_path_output,"w")
        
#         chunk_raw=pf.read(telemetry_package_size)
#         pcs_subsystem_position=1604
#         vBatAverage_pcs_subsystem_offset=750
#         vBatAverage_position_beg=pcs_subsystem_position+vBatAverage_pcs_subsystem_offset
#         vBatAverage_position_end=vBatAverage_position_beg+2
#         vBatAverage_chunk_raw=chunk_raw[vBatAverage_position_beg:vBatAverage_position_end]
        
#         while vBatAverage_chunk_raw:
            
#             vBatAverage_unpacked,=struct.unpack(">H",vBatAverage_chunk_raw)
#             vBatAverage_engineering_value=float(vBatAverage_unpacked)*0.01873128+(-38.682956)
#             print("=============================================================================")
#             print(f"VOLTAGE BATTERY AVERAGE - UNPACKED: {vBatAverage_unpacked}")
#             print("-----------------------------------------------------------------------------")
#             print(f"VOLTAGE BATTERY AVERAGE - ENGINEERING VALUE: {vBatAverage_engineering_value}")
#             print("=============================================================================")

#             pfvBatAverage.write(f"{vBatAverage_engineering_value:.5f};")

#             chunk_raw=pf.read(telemetry_package_size)
#             vBatAverage_chunk_raw=chunk_raw[vBatAverage_position_beg:vBatAverage_position_end]

#         pf.close()
#         pfvBatAverage.close()

#         file_path_visualize="vBatAverage_Engineering_Values.csv"
#         pfvBatAverage=open(file_path_visualize,"rb")

#         records=int(packages)
#         print(f"PACKAGES: {packages}")
#         print(f"RECORDS TO VISUALIZE: {records}")
#         file_size_visualize=os.path.getsize(file_path_visualize)
#         print(f"FILE SIZE: {file_size_visualize}")
#         vBatAverage_engineering_values=pfvBatAverage.read()
#         pfvBatAverage.close()

#         vBatAverage_string=vBatAverage_engineering_values.decode("utf-8")
#         vBatAverage_engineering_array=vBatAverage_string.split(";")

#         vBatAverage_dataframe=pd.DataFrame({"vBatAverage": vBatAverage_engineering_array})
#         vBatAverage_dataframe["vBatAverage"]=pd.to_numeric(vBatAverage_dataframe["vBatAverage"], errors="coerce")

#         vBatAverage_dataframe["package"]=vBatAverage_dataframe.index.values

#         print("============================================================")
#         print("\tPCS SUBSYSTEM TELEMETRY - VOLTAGE BATTERY AVERAGE")
#         print("============================================================")
#         print(vBatAverage_dataframe)
#         print("============================================================")

#         # USE PLOT() METHOD OF DATAFRAME FOR DATA VISUALIZATION.
#         plt.figure(figsize=(10, 5), dpi=150)
#         ax = plt.gca()
#         vBatAverage_dataframe.plot(x='package', y='vBatAverage', ax=ax)
#         ax.set_title("PCS SUBSYSTEM TELEMETRY - VOLTAGE BATTERY AVERAGE")
#         ax.set_xlabel("PACKAGES")
#         ax.set_ylabel("ENGINEERING VALUES")
#         plt.savefig("PCS_SUBSYSTEM_TELEMETRY-VOLTAGE_BATTERY_AVERAGE.jpg")
#         plt.show()

# def part2():

#     file_path_input="CGSS_20150603_091700_10020150603085920_SACD_HKTMST.bin"
#     file_size=os.path.getsize(file_path_input)
#     telemetry_package_size=4000 # Bytes

#     rest=file_size%telemetry_package_size
#     print(f"FILE SIZE: {file_size}")
#     print(f"TELEMETRY PACKAGE SIZE: {telemetry_package_size}")
#     print(f"REST PACKAGES: {rest}")
    
#     if not rest:

#         packages=file_size/telemetry_package_size
#         print(f"PACKAGES: {packages}")

#         pf=open(file_path_input,"rb")

#         file_path_output="obt_Engineering_Values.csv"
#         pfobt=open(file_path_output,"w")
        
#         chunk_raw=pf.read(telemetry_package_size)
#         cdh_subsystem_position=8
#         obt_offset=92
#         obt_position_beg=cdh_subsystem_position+obt_offset
#         obt_position_end=obt_position_beg+4
#         obt_chunk_raw=chunk_raw[obt_position_beg:obt_position_end]
        
#         # obt_timestamp,=struct.unpack(">I",obt_chunk_raw)
#         # obt_utc=datetime.fromtimestamp(obt_timestamp)
#         # print("=============================================================================")
#         # print(f"ON BOARD TIME - UNPACKED IN TIMESTAMP: {obt_timestamp}")
#         # print("-----------------------------------------------------------------------------")
#         # print(f"ON BOARD TIME - UTC DATE TIME: {obt_utc}")
#         # print("=============================================================================")

#         while obt_chunk_raw:
            
#             obt_timestamp,=struct.unpack(">I",obt_chunk_raw)
#             obt_utc=datetime.fromtimestamp(obt_timestamp)
#             print("=============================================================================")
#             print(f"ON BOARD TIME - UNPACKED IN TIMESTAMP: {obt_timestamp}")
#             print("-----------------------------------------------------------------------------")
#             print(f"ON BOARD TIME - UTC DATE TIME: {obt_utc}")
#             print("=============================================================================")

#             pfobt.write(f"{obt_utc};")
            
#             chunk_raw=pf.read(telemetry_package_size)
#             obt_chunk_raw=chunk_raw[obt_position_beg:obt_position_end]

#         pf.close()
#         pfobt.close()

#         file_path_visualize="obt_Engineering_Values.csv"
#         pfobt=open(file_path_visualize,"rb")

#         records=int(packages)
#         print(f"PACKAGES: {packages}")
#         print(f"RECORDS TO VISUALIZE: {records}")
#         file_size_visualize=os.path.getsize(file_path_visualize)
#         print(f"FILE SIZE: {file_size_visualize}")
#         obt_utc_values=pfobt.read()
#         pfobt.close()

#         obt_utc_datetime_string=obt_utc_values.decode("utf-8")
#         obt_utc_array=obt_utc_datetime_string.split(";")

#         obt_utc_dataframe=pd.DataFrame({"obt_utc": obt_utc_array})
#         obt_utc_dataframe["obt_utc"]=pd.to_datetime(obt_utc_dataframe["obt_utc"], errors="coerce")

#         obt_utc_dataframe["package"]=obt_utc_dataframe.index.values

#         print("============================================================")
#         print("\tCDH SUBSYSTEM TELEMETRY - ON BOARD TIME")
#         print("============================================================")
#         print(obt_utc_dataframe)
#         print("============================================================")

if __name__ == "__main__":

    file_path_input="CGSS_20150603_091700_10020150603085920_SACD_HKTMST.bin"
    file_size=os.path.getsize(file_path_input)
    telemetry_package_size=4000 # Bytes

    rest=file_size%telemetry_package_size
    # print(f"FILE SIZE: {file_size}")
    # print(f"TELEMETRY PACKAGE SIZE: {telemetry_package_size}")
    # print(f"REST PACKAGES: {rest}")
    
    if not rest:

        packages=file_size/telemetry_package_size
        # print(f"PACKAGES: {packages}")

        pf=open(file_path_input,"rb")

        file_path_output="vBatAverage_Engineering_Values.csv"
        pfvBatAverage=open(file_path_output,"w")

        file_path_measurement_times="Voltage_Measurement_Times.csv"
        pfvmt=open(file_path_measurement_times,"w")
        
        chunk_raw=pf.read(telemetry_package_size)
        
        pcs_subsystem_position=1604
        vBatAverage_pcs_subsystem_offset=750
        vBatAverage_position_beg=pcs_subsystem_position+vBatAverage_pcs_subsystem_offset
        vBatAverage_position_end=vBatAverage_position_beg+2
        
        cdh_subsystem_position=8
        obt_offset=92
        obt_position_beg=cdh_subsystem_position+obt_offset
        obt_position_end=obt_position_beg+4
        
        while chunk_raw:
            
            vBatAverage_chunk_raw=chunk_raw[vBatAverage_position_beg:vBatAverage_position_end]
            vBatAverage_unpacked,=struct.unpack(">H",vBatAverage_chunk_raw)
            vBatAverage_engineering_value=float(vBatAverage_unpacked)*0.01873128+(-38.682956)
            
            obt_chunk_raw=chunk_raw[obt_position_beg:obt_position_end]
            obt_timestamp,=struct.unpack(">I",obt_chunk_raw)
            obt_utc=datetime.fromtimestamp(obt_timestamp)

            # print("=============================================================================")
            # print(f"VOLTAGE BATTERY AVERAGE - UNPACKED: {vBatAverage_unpacked}")
            # print(f"ON BOARD TIME - UNPACKED IN TIMESTAMP: {obt_timestamp}")
            # print("-----------------------------------------------------------------------------")
            # print(f"VOLTAGE BATTERY AVERAGE - ENGINEERING VALUE: {vBatAverage_engineering_value}")
            # print(f"ON BOARD TIME - UTC DATE TIME: {obt_utc}")
            # print("=============================================================================")

            pfvBatAverage.write(f"{vBatAverage_engineering_value:.5f};")
            
            pfvmt.write(f"{obt_utc};{vBatAverage_engineering_value}\n")
            
            chunk_raw=pf.read(telemetry_package_size)

        pf.close()
        pfvBatAverage.close()
        pfvmt.close()

        file_path_visualize="vBatAverage_Engineering_Values.csv"
        pfvBatAverage=open(file_path_visualize,"rb")

        records=int(packages)
        # print(f"PACKAGES: {packages}")
        # print(f"RECORDS TO VISUALIZE: {records}")
        file_size_visualize=os.path.getsize(file_path_visualize)
        # print(f"FILE SIZE: {file_size_visualize}")
        vBatAverage_engineering_values=pfvBatAverage.read()
        pfvBatAverage.close()

        vBatAverage_string=vBatAverage_engineering_values.decode("utf-8")
        vBatAverage_engineering_array=vBatAverage_string.split(";")

        vBatAverage_dataframe=pd.DataFrame({"vBatAverage": vBatAverage_engineering_array})
        vBatAverage_dataframe["vBatAverage"]=pd.to_numeric(vBatAverage_dataframe["vBatAverage"], errors="coerce")

        vBatAverage_dataframe["package"]=vBatAverage_dataframe.index.values

        # print("============================================================")
        # print("\tPCS SUBSYSTEM TELEMETRY - VOLTAGE BATTERY AVERAGE")
        # print("============================================================")
        # print(vBatAverage_dataframe)
        # print("============================================================")

        # USE PLOT() METHOD OF DATAFRAME FOR DATA VISUALIZATION.
        plt.figure(figsize=(10, 5), dpi=150)
        ax = plt.gca()
        vBatAverage_dataframe.plot(x='package', y='vBatAverage', ax=ax)
        ax.set_title("PART 1 - PCS SUBSYSTEM TELEMETRY - VOLTAGE BATTERY AVERAGE")
        ax.set_xlabel("PACKAGES")
        ax.set_ylabel("ENGINEERING VALUES")
        plt.savefig("PCS_SUBSYSTEM_TELEMETRY-VOLTAGE_BATTERY_AVERAGE.jpg")
        
        file_path_visualize="Voltage_Measurement_Times.csv"
        pfvmt=open(file_path_visualize,"rb")

        records=int(packages)
        #print(f"PACKAGES: {packages}")
        #print(f"RECORDS TO VISUALIZE: {records}")
        file_size_visualize=os.path.getsize(file_path_visualize)
        #print(f"FILE SIZE: {file_size_visualize}")
        vBatAverage_engineering_values=pfvmt.read()
        pfvmt.close()

        vBatAverage_string=vBatAverage_engineering_values.decode("utf-8")
        #print(f"vBatAverage_string: {vBatAverage_string}")
        records_array=vBatAverage_string.split("\r\n")
        #print(f"records_array: {records_array}")

        vBatAverage_engineering_array=[]
        obt_utc_array=[]
        for record in records_array:

            record_values=record.split(";")
            #print(f"Record values: {record_values}")
            if (len(record_values)==2):

                obt_utc_value=record_values[0]
                vBatAverage_engineering_value=record_values[1]
                vBatAverage_engineering_array.append(vBatAverage_engineering_value)
                obt_utc_array.append(obt_utc_value)

        voltage_measurements_dataframe=pd.DataFrame({"obt_utc": obt_utc_array, "vBatAverage": vBatAverage_engineering_array})
        voltage_measurements_dataframe["vBatAverage"]=pd.to_numeric(voltage_measurements_dataframe["vBatAverage"], errors="coerce")
        voltage_measurements_dataframe["obt_utc"]=pd.to_datetime(voltage_measurements_dataframe["obt_utc"], errors="coerce")
        
        # print("============================================================")
        # print("\tVOLTAGE MEASUREMENTS TIMES")
        # print("------------------------------------------------------------")
        # print(voltage_measurements_dataframe)
        # print("============================================================")

        # USE PLOT() METHOD OF DATAFRAME FOR DATA VISUALIZATION.
        plt.figure(figsize=(10, 5), dpi=150)
        ax2 = plt.gca()
        voltage_measurements_dataframe.groupby(voltage_measurements_dataframe["obt_utc"].dt.hour)["vBatAverage"].min().plot(
            x='obt_utc', y="vBatAverage", ax=ax2
        )
        voltage_measurements_dataframe.groupby(voltage_measurements_dataframe["obt_utc"].dt.hour)["vBatAverage"].mean().plot(
            x='obt_utc', y="vBatAverage", ax=ax2
        )
        voltage_measurements_dataframe.groupby(voltage_measurements_dataframe["obt_utc"].dt.hour)["vBatAverage"].max().plot(
            x='obt_utc', y="vBatAverage", ax=ax2
        )
        ax2.set_title("PART 2 - VOLTAGE MEASUREMENTS TIMES")
        ax2.set_xlabel("HOUR OF THE DAY")
        ax2.set_ylabel("VOLTAGE ENGINEERING VALUES")
        plt.legend(['min per hour', 'mean per hour', 'max per hour'])
        plt.savefig("VOLTAGE_MEASUREMENTS_TIMES.jpg")
        plt.show()