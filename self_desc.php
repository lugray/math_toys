<?php
$base = 2;
if (isset($argv[1])){
  $base = $argv[1];
}

function simple_add(&$digits, $incdigit) {
  global $base;
  if ($incdigit < 0) {
    return FALSE;
  }
  if ($digits[$incdigit] < $base - 1) {
    $digits[$incdigit]++;
    return TRUE;
  }
  else {
    $digits[$incdigit]=0;
    return simple_add($digits, $incdigit - 1);
  }
}

function increase(&$digits) {
  global $base;
  if ($digits[$base-1] > 0){
    $digits[$base-1]--;
    if (!simple_add($digits, $base-2)){
      return FALSE;
    }
    $digits[$base-1] += $base - array_sum($digits);
    return TRUE;
  }
  else{
    $incdigit = $base - 2;
    while ($digits[$incdigit] == 0) {
      $incdigit--;
      if ($incdigit < 0) {
        echo "Really?";
        return FALSE;
      }
    }
    $digits[$incdigit] = $base - 1;
    if (!simple_add($digits, $incdigit)) {
      return FALSE;
    }
    $digits[$base-1] = $base - array_sum($digits);
    return TRUE;
  }
}

for ($base = 2; $base <= 36; $base++) {

echo 'Base: ' . $base . ':' . PHP_EOL;

$digits = array_fill(0, $base, 0);
$digits[$base-2] = 1;
$digits[$base-1] = $base - 1;
$success = FALSE;

do {
  $counts = array_fill(0, $base, 0);
  foreach ($digits as $digit) {
    $counts[$digit]++;
  }
  if ($digits == $counts) {
    $output = $digits;
    foreach ($output as $key => $value) {
      if ($value > 9) {
        $output[$key] = chr($value - 10 + ord('A'));
      }
    }
    echo implode($output) . PHP_EOL;
    $success = TRUE;
  }
} while (increase($digits));

if (!$success) {
  echo 'No solutions.' . PHP_EOL;
}

echo PHP_EOL;

}