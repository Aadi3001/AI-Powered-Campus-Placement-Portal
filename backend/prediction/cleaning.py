def clean_dataframe(df):
    """
    Basic cleaning for the training table.
    Returns (cleaned_copy, report). The report says how many rows each
    step removed, so nothing is dropped silently.
    """
    report = {'rows_in': len(df)}
    df = df.copy()

    # 1. Rows missing any value can't be used for training
    before = len(df)
    df = df.dropna()
    report['dropped_missing'] = before - len(df)

    # 2. One row per application
    before = len(df)
    df = df.drop_duplicates(subset='application_id')
    report['dropped_duplicates'] = before - len(df)

    # 3. Values that are impossible on their scale
    before = len(df)
    valid = (
        df['cgpa'].between(0, 10)
        & df['job_min_cgpa'].between(0, 10)
        & df['skill_match_percentage'].between(0, 100)
    )
    df = df[valid]
    report['dropped_out_of_range'] = before - len(df)

    report['rows_out'] = len(df)
    return df.reset_index(drop=True), report