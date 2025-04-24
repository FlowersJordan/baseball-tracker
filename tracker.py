import csv
import os

CSV_FILE = "data/mlb_stats.csv"


def load_players():
    players = []

    with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:

                if int(row["PA"]) < 100:
                    continue  # Skip low sample size

                player = {
                    "name": row["Player"],
                    "team": row["Team"],
                    "HR": int(row["HR"]),
                    "RBI": int(row["RBI"]),
                    "BA": float(row["BA"]),
                    "PA": int(row["PA"])
                }

                players.append(player)
            except ValueError:
                continue
    return players


def player_search(players):
    query = input("Enter Player Name: ").strip().lower()

    results = [p for p in players if query in p["name"].lower()]

    if not results:
        print("No Players were found.")
        return
    
    print(f"\n Results for '{query}':")
    for p in results:
        print(f"{p['name']} ({p['team']}) - HR: {p['HR']}, RBI: {p['RBI']}, BA: {p['BA']:.3f}")




def show_top_players(players, stat, top_n=10):
    sorted_players = sorted(players, key=lambda x: x[stat], reverse=True)

    print(f"\n Top {top_n} Players by {stat}:")
    for i, p in enumerate(sorted_players[:top_n], start=1):
        print(f"{i}. {p['name']} ({p['team']}) -- {stat}: {p[stat]}")


def export_leaderboard(players, stat, top_n=10):
    sorted_players = sorted(players, key=lambda x: x[stat], reverse=True)
    filename = f"output/top_{stat.lower()}.txt"

    os.makedirs("output", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"🏆 Top {top_n} Players by {stat}\n\n")
        for i, p in enumerate(sorted_players[:top_n], start=1):
            f.write(f"{i}. {p['name']} ({p['team']}) - {stat}: {p[stat]}\n")

    print(f"📄 Exported to {filename}")


def main_menu():
    players = load_players()

    while True:
        print("\n==== MLB STATS TRACKER ====")
        print("1. Show top players by Home Runs")
        print("2. Show top players by RBIs")
        print("3. Show top players by Batting Average")
        print("4. Search Player by Name")
        print("5. Export based on Stat")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        match choice:
            case "1":
                show_top_players(players, "HR")
            case "2":
                show_top_players(players, "RBI")
            case "3":
                show_top_players(players, "BA")
            case "4":
                player_search(players)
            case "5":
                stat = input("Export leaderboard by which stat (HR, RBI, BA)? ").strip().upper()
                if stat not in {"HR", "RBI", "BA"}:
                    print("❌ Invalid stat.")
                else:
                    export_leaderboard(players, stat)
            case "6":
                print("Exiting Stats Tracker.")
                break
            case _:
                print("Invalid choice. Please Try Again.")

if __name__ == "__main__":
    main_menu()


