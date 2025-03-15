from perm import permute
import pytest

def test_empty_collections():
    # Test empty list and set
    assert permute([]) == [[]]
    assert permute(set()) == [[]]
    
def test_single_element():
    # Test single element
    assert permute([1]) == [[1]]
    assert permute({1}) == [[1]]
    
def test_two_elements():
    # Test two elements
    list_result: list[list[int]] = permute([1, 2])
    set_result: list[list[int]] = permute({1, 2})
    
    assert len(list_result) == 2
    assert len(set_result) == 2
    assert [1, 2] in list_result
    assert [2, 1] in list_result
    assert [1, 2] in set_result
    assert [2, 1] in set_result
    
def test_three_elements():
    # Test three elements
    list_result = permute([1, 2, 3])
    set_result = permute({1, 2, 3})
    
    assert len(list_result) == 6
    assert len(set_result) == 6
    
    expected_perms: list[list[int]] = [
        [1, 2, 3], [1, 3, 2], 
        [2, 1, 3], [2, 3, 1], 
        [3, 1, 2], [3, 2, 1]
    ]
    
    for perm in expected_perms:
        assert perm in list_result
        assert perm in set_result

if __name__ == "__main__":
    test_empty_collections()
    test_single_element()
    test_two_elements()
    test_three_elements() 