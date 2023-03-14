import os
from time import sleep


def gravar_novo_sped(lista_sped, nome, dt_inicio, dt_fim):
    with open(f"speds_modificados\\{nome} {dt_inicio} {dt_fim}.txt", 'a', encoding='ansi') as novo_sped:
        for lista in lista_sped:
            novo_sped.write(lista)


def ler_efd_pis_cofins(arquivo_sped):
    with open(arquivo_sped, 'r', encoding='ansi') as sped:
        lista = sped.readlines()
    return lista


def string_to_float(valor):
    try:
        valor = valor.replace('.', '').replace(',', '.')
        valor = round(float(valor), 2)
    except:
        valor = 0
    return valor


def float_to_string(valor):
    valor = str(valor)
    valor = valor.replace('.', ',')
    return valor


def recalcular_impostos_pis_cofins_c170(lista_sped):
    novo_sped = []
    passou = False
    for lista in lista_sped:
        nova_lista = []
        passou = False
        if lista.split('|')[1] == '9999':
            novo_sped.append(lista)
            break
        registro = lista.split('|')[1]
        if registro == '0000':
            nome = lista.split('|')[8]
            dt_inicio = lista.split('|')[6]
            dt_fin = lista.split('|')[7]
        if registro == 'C100':
            valor_icms_c175 = lista.split('|')[22]
        if registro == 'C170':
            CST_Pis = lista.split('|')[25]
            if CST_Pis == '01':
                nova_lista = lista.split('|')
                valor_icms = string_to_float(nova_lista[15])
                vl_bc_pis = string_to_float(nova_lista[26])
                vl_bc_cofins = string_to_float(nova_lista[32])
                aliq_pis = string_to_float(nova_lista[27])
                aliq_cofins = string_to_float(nova_lista[33])
                if valor_icms:
                    vl_nova_bc_pis = round(vl_bc_pis - valor_icms, 2)
                    vl_nova_bc_cofins = round(vl_bc_cofins - valor_icms, 2)
                    valor_novo_pis = round((vl_nova_bc_pis * aliq_pis)/100, 2)
                    valor_novo_cofins = round(
                        (vl_nova_bc_cofins * aliq_cofins)/100, 2)

                    nova_lista[26] = float_to_string(
                        vl_nova_bc_pis) if vl_nova_bc_pis > 0 else 0
                    nova_lista[32] = float_to_string(
                        vl_nova_bc_cofins) if vl_nova_bc_cofins > 0 else 0
                    nova_lista[30] = float_to_string(
                        valor_novo_pis) if valor_novo_pis > 0 else 0
                    nova_lista[36] = float_to_string(
                        valor_novo_cofins) if valor_novo_cofins > 0 else 0
                    novo_sped.append('|'.join([str(i) for i in nova_lista]))
                    passou = True
        if registro == 'C175':
            CST_Pis = lista.split('|')[5]
            if CST_Pis == '01':
                nova_lista = lista.split('|')
                valor_icms_c175 = string_to_float(valor_icms_c175)
                vl_bc_pis = string_to_float(nova_lista[6])
                vl_bc_cofins = string_to_float(nova_lista[12])
                aliq_pis = string_to_float(nova_lista[7])
                aliq_cofins = string_to_float(nova_lista[13])
                if valor_icms_c175:
                    vl_nova_bc_pis = round(vl_bc_pis - valor_icms_c175, 2)
                    vl_nova_bc_cofins = round(
                        vl_bc_cofins - valor_icms_c175, 2)
                    valor_novo_pis = round((vl_nova_bc_pis * aliq_pis)/100, 2)
                    valor_novo_cofins = round(
                        (vl_nova_bc_cofins * aliq_cofins)/100, 2)

                    nova_lista[6] = float_to_string(
                        vl_nova_bc_pis) if vl_nova_bc_pis > 0 else 0
                    nova_lista[12] = float_to_string(
                        vl_nova_bc_cofins) if vl_nova_bc_cofins > 0 else 0
                    nova_lista[10] = float_to_string(
                        valor_novo_pis) if valor_novo_pis > 0 else 0
                    nova_lista[16] = float_to_string(
                        valor_novo_cofins) if valor_novo_cofins > 0 else 0
                    print(nova_lista)
                    novo_sped.append('|'.join([str(i) for i in nova_lista]))
                    passou = True

        if not passou:
            novo_sped.append(lista)
    return novo_sped, nome, dt_inicio, dt_fin


if __name__ == '__main__':
    # deletar speds anteriores
    for diretorio, subpastas, arquivos in os.walk('speds_modificados'):
        for arquivo in arquivos:
            arquivo_sped = os.path.join(diretorio, arquivo)
            os.remove(arquivo_sped)
            sleep(2)

    # percorrer pasta com os arquivos sped
    for diretorio, subpastas, arquivos in os.walk('speds'):
        for arquivo in arquivos:
            arquivo_sped = os.path.join(diretorio, arquivo)
            lista = ler_efd_pis_cofins(arquivo_sped)
            novo_sped, nome, dt_inicio, dt_fim = recalcular_impostos_pis_cofins_c170(
                lista)
            gravar_novo_sped(novo_sped, nome, dt_inicio, dt_fim)
