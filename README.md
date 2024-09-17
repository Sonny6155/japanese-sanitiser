# japanese-sanitiser

Script for detecting issues in Japanese text. Initially designed to help lyric
transcription (but never used), building from santisation code of a previous
project.

Has limited transposition abilities for between half and fullwidth latin.

TODO:
- Displayer for all filtered and unfiltered chars in the used Unicode blocks.
- Function to transpose "、", common quote brackets to kana (don't bother with reverse)
- Proper file/line trimming
- Non-warning (formatting) detection of JP punctuation after EN and vice versa
- Detection of untrimmed lines
