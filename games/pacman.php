<?php 
    if (!isset($name)) 
        die("This is not the site you are looking for.");
?>

<div class="popis">
    <h3>Pacman</h3>
    <p>
    Obtiažnosť: pokročilá<br/>
    Autor: Jano<br/>
    Zdrojový kód: <?php echo "<a href=\"$path/$name.zip\">$name.zip</a>"; ?> <br/>
    </p>
    <p>
    Túto hru určite poznáte, vašou úlohou je pomocou šípok na klávesnici ovládať postavičku 
    a zjesť čo najviac jedla. Pozor, nenechajte sa zjesť duchom (Avšak ak je svetlý, 
    môžete is dať ho dať ako dezert.)

    Skúste dorobiť viac levelov, životy a čo vás len napadne.
    </p>
</div>
<div class="obrazok">
  <?php
    $src = "$path/screen-$name.png";
    echo "<a href=\"$src\"><img src=\"$src\" alt=\"screen-$name.png\" /></a>"; 
  ?>
</div>
<br class="clear"/>
