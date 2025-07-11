def update_array(target_arr, index, value, new_size=None):
    # Resize if new_size is provided
    if new_size is not None:
        if new_size < len(target_arr):
            target_arr = target_arr[:new_size]
        else:
            target_arr.extend([0] * (new_size - len(target_arr)))

    # Ensure the list is long enough to accommodate the index
    if index >= len(target_arr):
        target_arr.extend([0] * (index - len(target_arr) + 1))

    # Update the value at the specified index
    target_arr[index] = int(value)
    return
