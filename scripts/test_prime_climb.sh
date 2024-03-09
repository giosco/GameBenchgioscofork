cd /Users/ottavia/Downloads/GameBenchgioscofork
python api/play_game.py \
    --agent_1_path agents.gpt.GPT4Text \
    --agent_2_path agents.gpt.ChainOfThought \
    --game_path games.prime_climb.prime_climb.PrimeClimbGame \
    --show_state \
    --num_matches 50