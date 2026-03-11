from src.main import run_agent_loop

if __name__ == '__main__':
    print ('Welcome to the first AI Weather Assistant.')
    while True:
        user_input = input ('\nYou : ')

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("AI: Goodbye! See you tomorrow.")
            break
     
        output = run_agent_loop (user_input, max_iterations=5)
        print ('Response : ', output)