<?php 
    if (!isset($name)) 
        die("This is not the site you are looking for.");
?>

<div class="popis">
    <h3>Ryba</h3>
    <p>
    Obtiažnosť: pokročilá<br/>
    Autor: Jano<br/>
    Zdrojový kód: <?php echo "<a href=\"$path/$name.zip\">$name.zip</a>"; ?> <br/>
    </p>
    <p>
    Rybu ovládate šípkami. Hra sa snaží trocha napodobňovať (ale len napodobňovať) reálnu
    fyziku. Pohyb je plynulý funguje trenie a dokonca sa ryba správa inak pod vodou a nad 
    hladinou. Zrážky sú realistickejšie. Jedlo sa postupne rozmočí.

    Ak si trufate, môžete z toho skúsiť spraviť hru. Pridajte rybe hladnosť, dajte tomu nejaký cieľ,
    rozšírte repertoár objektov.
    </p>
</div>
<div class="obrazok">
  <?php
    $src = "$path/screen-$name.png";
    echo "<a href=\"$src\"><img src=\"$src\" alt=\"screen-$name.png\" /></a>"; 
  ?>
</div>
<br class="clear"/>
