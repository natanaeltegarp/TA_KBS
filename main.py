import json

# Function to load JSON data from file
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
        
# Function to calculate average stats for a given team
def calculate_average_stats(data, team_name):
    stats_sum = {}
    count = 0
    
    for game in data:
        home_team = game["home_team"]
        away_team = game["away_team"]
        
        if home_team["name"] == team_name:
            stats = home_team["team_stats"]
        elif away_team["name"] == team_name:
            stats = away_team["team_stats"]
        else:
            continue
        
        for key, value in stats.items():
            if key in ["name", "week"]:
                continue 
            if key not in stats_sum:
                stats_sum[key] = 0.0
            stats_sum[key] += float(value)
        
        count += 1
    
    if count == 0:
        print(f"No games found for team {team_name}")
        return

    average_stats = {key: value / count for key, value in stats_sum.items()}

    # Apply weights
    weights = {
        "score": 10,
        "fouls": -5,
        "corners": 5,
        "touches": 3,
        "crosses": 4,
        "tackles": 6,
        "interceptions": 7,
        "aerials_won": 5,
        "clearances": 5,
        "offsides": -3,
        "goal_kicks": 2,
        "throw_ins": 2,
        "long_balls": 3
    }

    weighted_stats = {key: average_stats[key] * weights[key] for key in average_stats if key in weights}
    
    total_weighted_score = sum(weighted_stats.values())

    #Display
    # print(f"Weighted average stats for {team_name}:")
    # for key, value in weighted_stats.items():
    #     print(f"{key}: {value:.2f}")
    # print(f"Total weighted score for {team_name}: {total_weighted_score:.2f}")
    
    return total_weighted_score
    
# Main function
def main():
    file_path = 'dataset.json'
    data = load_json(file_path)

    home_team = input("Enter the home team name: ")
    away_team = input("Enter the away team name: ")
    
    home_weighted_score = calculate_average_stats(data, home_team)
    away_weighted_score = calculate_average_stats(data, away_team)
    
    home_win_percentage = home_weighted_score / (home_weighted_score + away_weighted_score)*100
    away_win_percentage = away_weighted_score / (home_weighted_score + away_weighted_score)*100

    print(f"{home_team} win percentage: {home_win_percentage:.2f}%")
    print(f"{away_team} win percentage: {away_win_percentage:.2f}%")
    
if __name__ == "__main__":
    main()
