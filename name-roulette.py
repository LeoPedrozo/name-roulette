import itertools
import threading
import time
import sys
import os
import argparse
import pandas as pd

def loading_animation():
    done = False
    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break

            sys.stdout.write('\rBuscando al ganador... ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(1)
    done = True

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_choose_again():
    again = input("\nVolver a elegir? [Y/N]: ")
    if (again == 'y' or again == 'Y'):
        return
    elif again == 'n' or again == 'N':
        print("\nPrograma finalizado.")
        sys.exit(0)
    else:
        print("\nEntrada invalida: tipea Y para yes o N para no.")
        ask_choose_again()

def draw_name(df, amount, repeat, display):
    while not df.empty:
        clear_terminal()
        loading_animation()
        clear_terminal()
        chosen_name = []
        for i in range(0, amount):
            if df.empty:
                break
            chosen_name.append(df.loc[df.sample().index[0], 'Participantes'])
            if not repeat:
                df = df[df["Participantes"].str.contains(chosen_name[i])==False]
        if display and not df.empty:
            print(df)
        else:
            print('---------------------------- ')
            print('|    SORTEO DE              |')
            print('---------------------------- ')
            print(f"\nGanadores: {', '.join(chosen_name)}")
        ask_choose_again()
    else:
        print("\nEl programa ha finalizado.\nLa lista de nombres esta vacia.")
        sys.exit(0)

def get_names(filename):
    try:
        names_df = pd.read_csv(filename, sep=",", header=None, names=["Participantes"])
        names_df['Participantes'] = names_df['Participantes'].astype('string')
        return names_df
    except FileNotFoundError:
        print(f"\nFile '{filename}' does not exist.")
        if filename[-4:] != '.csv' and filename[-4:] != '.txt':
            print(f"Please include file type, e.g., {filename}.txt or {filename}.csv.")
        sys.exit(0)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Name Roulette v2.1.0. A random picker for names. A digital terminal script based on the game spin the bottle.')

    parser.add_argument(
        'file',
        metavar='filename',
        type=str,
        help='Files accepted are csv and txt files. Add the filename of the text or csv file containing the names as an argument, e.g., fileName.csv. Each name should be entered in a new line. You may refer to the README.md to see more examples.'
    )

    parser.add_argument(
        'amount',
        metavar='amount',
        nargs='?',
        default=1,
        type=int,
        help='numero de personas a ser elegidas ganadoras en el sorteo.'
    )

    parser.add_argument(
        '--repeat',
        action="store_true",
        required=False,
        help='Permite que el nombre siga utilizandose para el sorteo. No incluir --repeat removera al usuario de la lista una vez que salga ganador.'
    )

    parser.add_argument(
        '--display',
        action="store_true",
        required=False,
        help='Mostrar la lista de nombres.'
    )

    args = parser.parse_args()
    draw_name(get_names(args.file), args.amount, args.repeat, args.display)

