<?php 
    if (!isset($name)) 
        die("This is not the site you are looking for.");
?>

<div class="popis">
    <h3>Hadík</h3>
    <p>
    Obtiažnosť: pokročilá<br/>
    Autor: Mário<br/>
    Zdrojový kód: <?php echo "<a href=\"$path/$name.zip\">$name.zip</a>"; ?> <br/>
    </p>
    <p>
    V tejto hre šípkamy ovládate nenásytného hadíka. Hadík jedením rastie a bezhlavo sa rúti proti stenám.
    Snažte sa, aby vám hadík prežil čo najdlhšie.

    V tejto hre je vytvorených viac levelov, úvodné menu a aj tabuľka highscore, do ktorej sa dá zapisovať.
    </p>
</div>
<div class="obrazok">
  <?php
    $src = "$path/screen-$name.png";
    echo "<a href=\"$src\"><img src=\"$src\" alt=\"screen-$name.png\" /></a>"; 
  ?>
</div>
<br class="clear"/>
