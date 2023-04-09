# Problem Set 4A
# Name: Marcos Ortiz
# Collaborators: none
# Time Spent: 1:30

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # Initialize a list of permutations
    permutations = []

    # Base case:
    # There is only one character in the sequence,
    # so there is only one permutation to return
    if len(sequence) == 1:
        permutations.append(sequence)

    # Inductive step:
    # There are n characters in the sequence
    else:
        # We hold on to the first chacter
        hold_char = sequence[0]

        # For each permutation of the remaining n-1 characters
        for item in get_permutations(sequence[1:]):
            # We insert the held leter at each possible position
            # and add that permutation of n characters to our list
            for i in range(len(item)+1):
                permutations.append(item[:i]+hold_char+item[i:])

    # Return the updated list of permutations
    return permutations

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)

    example1 = 'abc'
    print('Input:', example1)
    print('Expected Output:', ['abc', 'bac', 'bca', 'acb', 'cab', 'cba'])
    print('Actual Output:  ', get_permutations(example1))

    example2 = 'MIT'
    print('Input:', example2)
    print('Expected Output:', ['MIT', 'IMT', 'ITM', 'MTI', 'TMI', 'TIM'])
    print('Actual Output:  ', get_permutations(example2))

    example3 = 'AB'
    print('Input:', example3)
    print('Expected Output:', ['AB', 'BA'])
    print('Actual Output:  ', get_permutations(example3))
