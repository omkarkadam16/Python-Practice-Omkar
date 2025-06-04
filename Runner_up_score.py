if __name__ == '__main__':
    # Read scores as a list of integers
    arr = list(map(int, input().split()))
    # Remove duplicates using set and sort in descending order
    unique_score =sorted(set(arr),reverse=True)
    # Print the second-highest score
    print(unique_score[1])