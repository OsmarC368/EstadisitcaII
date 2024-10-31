import cutie

def main():
    options = [f'Choice {i}' for i in range(1, 5)]
    chosen_idx = cutie.select(options, )
    chosen = options[chosen_idx]
    print(chosen_idx)

if __name__ == "__main__":
    main()