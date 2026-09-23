# ComfyUI-QwenImage-PhotoStyles

A single ComfyUI node — **PE-T2I Photo Style Prompt** — that turns a short prompt into a
rich, styled one for **Qwen-Image-2.1**.

Pick a **photographic style** from a dropdown (17 styles), type a short prompt, and the node
sends it to a **PE-T2I rewriter** (any OpenAI-compatible endpoint) together with that style's
sheet. It returns a long English prompt, a matching **negative prompt**, and the **width /
height** for the aspect ratio the rewriter chose.

Each style is described as **camera language + mood** — never a photographer's name. Your
subject, and whatever text / counts / colours / positions you specify, stay yours; the style
only decides what you left open. The shorter your prompt, the more the style shows through.

> **This is not a model loader.** It only produces text (prompt / negative) and two integers
> (width / height). It has nothing to do with GGUF / NVFP4 / fp8 / bf16 — those only matter for
> the loader nodes downstream. Use it with any Qwen-Image-2.1 setup, in any format.

## Where this node sits

It stands **at the very front** and only shapes text: it takes your short line + the chosen
style, has the PE-T2I rewriter expand it, and hands the finished prompt / negative / size to the
ordinary Qwen-Image-2.1 nodes. It never loads a model or touches a pixel — think of it as the
*art director* that writes the shot; the camera (the DiT) takes it.

```
   your short line   +   style dropdown
              |
              v
 +--------------------------------------+
 |   PE-T2I Photo Style Prompt  (THIS)  |   <- text only, seconds, no VRAM
 |   short line + style sheet --> PE-T2I |
 |   out: long prompt . negative . size |
 +--------------------------------------+
     | prompt / negative        | width / height
     v                          v
 TextEncodeQwenImage21      EmptyLatentImage
     |  (encode -> cond)         | (make canvas)
     +---------->  KSampler (DiT denoise)  <--------+
                        |
                        v
                    VAEDecode  -->  final image
```

## Gallery

**Every image below is the whole prompt you write** — pick a style, type one short line like the
caption, and this is what comes out. Two photos and two "posters" per style; nothing was
hand-tuned. (Generated with this node on a quantized Qwen-Image-2.1 setup.)

### Black Fury

<table>
<tr>
<td width="25%" valign="top"><img src="examples/black_fury_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a stray dog snaps its head around in a pitch-black alley after midnight rain&rdquo;</i><br>&#12300;午夜雨後漆黑的巷子，一隻野狗猛然回頭、雙眼直盯鏡頭&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/black_fury_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a blurred face lurches toward the camera through a dense crowd under harsh neon&rdquo;</i><br>&#12300;刺眼霓虹下擁擠的人潮，一張模糊的臉朝鏡頭踉蹌逼近&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/black_fury_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a gritty B&W gig poster, huge distressed title “NOISE”, a blurred running figure&rdquo;</i><br>&#12300;粗粒黑白的地下樂團演出海報，巨大斑駁的標題文字「NOISE」，下方一個模糊奔跑的身影&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/black_fury_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a B&W street-photography exhibition poster, bold title “STREET”, a lone backlit figure&rdquo;</i><br>&#12300;黑白街拍攝影展海報，頂端粗體標題「STREET」，中央一個逆光孤影被黑暗吞沒&#12301;</sub></td>
</tr>
</table>

### Geometry of Light

<table>
<tr>
<td width="25%" valign="top"><img src="examples/geometry_of_light_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a Tokyo street, hard evening light slicing a narrow alley, a passer-by casting a long shadow (B&W)&rdquo;</i><br>&#12300;東京街頭，一道強烈夕陽斜光切過狹窄巷弄，一個行人拉出長長的影子，黑白高反差&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/geometry_of_light_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a tiny figure at the end of a long arcade, a blade of light slicing the columns&rdquo;</i><br>&#12300;長廊盡頭一個渺小的身影，一道光刃劈過整排廊柱&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/geometry_of_light_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a minimalist B&W exhibition poster, a Tokyo-street beam and long shadows, title “LIGHT AND SHADOW”&rdquo;</i><br>&#12300;極簡黑白攝影展海報，東京街頭一道光束與長影構成的幾何，大片留黑，底部小字標題「LIGHT AND SHADOW」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/geometry_of_light_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;an architecture-biennale poster, a beam and long shadows, title “Geometry”&rdquo;</i><br>&#12300;建築雙年展海報，一道光束與長影構成的幾何，頂端標題「幾何」&#12301;</sub></td>
</tr>
</table>

### Warm Documentary

<table>
<tr>
<td width="25%" valign="top"><img src="examples/warm_documentary_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a farmer’s rough hands cupping seedlings, a child watching at the field’s edge&rdquo;</i><br>&#12300;老農粗糙的雙手捧著秧苗，田邊一個孩子靜靜看著&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/warm_documentary_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;an old stall-keeper laughing among hanging vegetables under market lamplight&rdquo;</i><br>&#12300;燈光下的傳統菜攤，一位老闆娘在垂掛的蔬菜之間笑著&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/warm_documentary_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a humanist documentary exhibition poster, a warm B&W portrait, title “Land and People”&rdquo;</i><br>&#12300;人文紀實攝影展海報，一張溫暖的黑白肖像，底部標題「土地與人」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/warm_documentary_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a documentary film-festival poster, a close-up of working hands, title “HANDS”&rdquo;</i><br>&#12300;紀錄片影展海報，一雙勞動的手部特寫，上方標題「HANDS」&#12301;</sub></td>
</tr>
</table>

### White Leap

<table>
<tr>
<td width="25%" valign="top"><img src="examples/white_leap_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a dancer frozen at the peak of a leap, full body on pure white&rdquo;</i><br>&#12300;純白背景前，舞者在跳躍最高點被凝結的全身&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/white_leap_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;an extreme close-up of a deeply lined face, every pore sharp, eyes on the lens&rdquo;</i><br>&#12300;佈滿深刻皺紋的臉部大特寫，每個毛孔清晰、直視鏡頭&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/white_leap_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a pure-white minimalist fashion poster, a leaping dancer, vertical title “LEAP”&rdquo;</i><br>&#12300;純白極簡時尚海報，全身躍起的舞者，一側直排標題「LEAP」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/white_leap_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a B&W portrait-show poster, white ground, a razor-sharp face, title “FACE”&rdquo;</i><br>&#12300;黑白肖像展海報，白底、銳利的臉孔特寫，頂端標題「FACE」&#12301;</sub></td>
</tr>
</table>

### Corner Elegance

<table>
<tr>
<td width="25%" valign="top"><img src="examples/corner_elegance_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a woman folded elegantly into a bare studio corner, hands quietly clasped&rdquo;</i><br>&#12300;一位女子優雅地縮進空蕩的牆角，雙手安靜交疊&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/corner_elegance_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a single wilting tulip against a smooth grey seamless ground&rdquo;</i><br>&#12300;光滑的灰色背景前，一朵正在枯萎的鬱金香&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/corner_elegance_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a minimalist gallery poster, lots of white space, a quiet corner figure, title “CORNER”&rdquo;</i><br>&#12300;極簡藝廊海報，大片留白，角落一個安靜的身影，小字標題「CORNER」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/corner_elegance_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a still-life photobook poster, grey ground with a wilting tulip, title “STILL”&rdquo;</i><br>&#12300;靜物攝影集海報，灰底一朵枯萎鬱金香，底部細字標題「STILL」&#12301;</sub></td>
</tr>
</table>

### Cold Power

<table>
<tr>
<td width="25%" valign="top"><img src="examples/cold_power_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a commanding woman in heels, full figure, at the edge of a floodlit midnight pool&rdquo;</i><br>&#12300;深夜泛光燈的泳池邊，一位穿高跟鞋、氣場強大的女子全身站姿&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/cold_power_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a model leaning coldly against a sports car on a neon-wet street&rdquo;</i><br>&#12300;霓虹濕滑的街道旁，一位模特兒冷冷地倚著一輛跑車&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/cold_power_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a high-fashion magazine cover, a full-figure power stance, masthead “NOIR”&rdquo;</i><br>&#12300;高冷時尚雜誌封面，全身女子強勢站姿，頂端刊名「NOIR」與幾行小字&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/cold_power_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a B&W fashion poster, a woman descending marble stairs, vertical title “POWER”&rdquo;</i><br>&#12300;黑白時尚海報，大理石長階上俯視鏡頭走下的高挑女子，直排標題「POWER」&#12301;</sub></td>
</tr>
</table>

### Hyper Chic East

<table>
<tr>
<td width="25%" valign="top"><img src="examples/hyper_chic_east_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a photorealistic editorial shot, a full-figure model in a sleek contemporary designer gown, power stance&rdquo;</i><br>&#12300;寫實時尚雜誌大片，一位全身模特兒穿著剪裁俐落的當代設計師禮服，站在乾淨棚拍佈景前，強勢時尚站姿&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/hyper_chic_east_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a photorealistic fashion shot, a model in a fitted satin suit, clean studio, jewel-tone backdrop&rdquo;</i><br>&#12300;寫實時尚攝影，全身模特兒穿著合身絲緞套裝，乾淨棚燈，濃艷珠寶色背景，醒目時尚站姿&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/hyper_chic_east_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a photoreal fashion magazine cover, a full-figure model in modern haute couture, masthead “CHIC”&rdquo;</i><br>&#12300;寫實時尚雜誌封面，全身模特兒穿當代高訂禮服，乾淨棚拍珠寶色背景，頂部放簡潔刊名「CHIC」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/hyper_chic_east_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a high-colour fashion poster, a model in a minimal structured gown, side title “CHIC EAST”&rdquo;</i><br>&#12300;寫實高彩時尚海報，全身模特兒穿極簡結構感當代禮服，珠寶色背景，一側放簡潔標題「CHIC EAST」&#12301;</sub></td>
</tr>
</table>

### Private Diary

<table>
<tr>
<td width="25%" valign="top"><img src="examples/private_diary_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a small bunch of red flowers on a cluttered balcony against a bruised evening sky&rdquo;</i><br>&#12300;雜亂的陽台上一小束紅花，襯著泛紫的黃昏天空&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/private_diary_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;someone just woken, half-wrapped in sheets, lit by a hard close flash&rdquo;</i><br>&#12300;剛睡醒的人半裹在被單裡，被近距離的硬閃燈打亮&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/private_diary_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a private-snapshot photobook poster, an intimate flash snapshot, title “Diary”&rdquo;</i><br>&#12300;私寫真攝影集海報，閃燈直打的親密快照，底部手寫感標題「日記」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/private_diary_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;an indie photo-show poster, an overexposed flash close-up, title “DIARY”&rdquo;</i><br>&#12300;獨立寫真展海報，過曝的閃燈近景，頂端標題「DIARY」&#12301;</sub></td>
</tr>
</table>

### Color Behind Glass

<table>
<tr>
<td width="25%" valign="top"><img src="examples/color_behind_glass_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a lone red umbrella seen through a fogged, rain-streaked café window&rdquo;</i><br>&#12300;起霧又佈滿雨痕的咖啡館玻璃後，一把孤獨的紅傘&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/color_behind_glass_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a blurred street reflected in a steamed-up window, one warm light glowing&rdquo;</i><br>&#12300;起霧的窗上倒映著模糊的街景，只有一盞暖燈亮著&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/color_behind_glass_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a soft-colour exhibition poster, a blurred street behind a rainy window, title “GLASS”&rdquo;</i><br>&#12300;柔調彩色攝影展海報，隔著雨窗的模糊街景，底部細字標題「GLASS」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/color_behind_glass_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;an art-house film poster, a splash of red behind frosted glass, title “Rain”&rdquo;</i><br>&#12300;文青影展海報，霧面玻璃後一抹紅，直排標題「雨」&#12301;</sub></td>
</tr>
</table>

### Frozen Film Still

<table>
<tr>
<td width="25%" valign="top"><img src="examples/frozen_film_still_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a lone figure standing motionless in an empty suburban street at blue dusk&rdquo;</i><br>&#12300;藍色黃昏，空蕩郊區街道正中央一動不動站著的人&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/frozen_film_still_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a woman alone under the cold light of a deserted gas station at nightfall&rdquo;</i><br>&#12300;入夜無人的加油站，冷白燈光下獨自站著的女子&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/frozen_film_still_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a cinematic poster, a lone figure at blue dusk, film title “DUSK” with small credits&rdquo;</i><br>&#12300;電影感海報，藍調黃昏郊區、街心的孤立身影，底部片名「DUSK」與演職員小字&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/frozen_film_still_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;an indie film poster, a lone woman at a cold-lit gas station, title “Silence”&rdquo;</i><br>&#12300;獨立電影海報，冷光加油站的孤獨女子，頂端片名「靜默」&#12301;</sub></td>
</tr>
</table>

### Fairytale Giants

<table>
<tr>
<td width="25%" valign="top"><img src="examples/fairytale_giants_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a tiny figure gazing up at a flower taller than a house, petals like parasols&rdquo;</i><br>&#12300;一個渺小的人仰望比房子還高的巨大花朵，花瓣像陽傘&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/fairytale_giants_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a tiny traveller walking past a row of giant mushrooms on a pastel set&rdquo;</i><br>&#12300;一個渺小的旅人走過一排比人還高的巨大蘑菇，夢幻粉彩佈景&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/fairytale_giants_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a dreamy fashion-editorial poster, a tiny figure beside a giant flower, title “WONDER”&rdquo;</i><br>&#12300;夢幻時尚大片海報，巨大花朵旁的小小人物，花體標題「WONDER」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/fairytale_giants_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a fairytale-exhibition poster, a giant teacup and a sleeping girl, title “Land of Giants”&rdquo;</i><br>&#12300;童話展覽海報，巨大茶杯與熟睡的女孩，頂端標題「巨物奇境」&#12301;</sub></td>
</tr>
</table>

### Soft Everyday Light

<table>
<tr>
<td width="25%" valign="top"><img src="examples/soft_everyday_light_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a backlit child in a soft afternoon room, dust drifting in the light&rdquo;</i><br>&#12300;午後柔光的房間裡逆光的孩子，塵埃在光中漂浮&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/soft_everyday_light_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;the small back of a child running toward a pale, hazy summer sea&rdquo;</i><br>&#12300;一個孩子小小的背影，朝著淡霧色的夏日海奔去&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/soft_everyday_light_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a gentle lifestyle photobook poster, a backlit child and floating dust, title “Everyday Light”&rdquo;</i><br>&#12300;溫柔生活攝影集海報，逆光的孩子與漂浮的塵埃，底部細字「日常之光」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/soft_everyday_light_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a photo-exhibition poster, a small back running by a hazy sea, title “Summer”&rdquo;</i><br>&#12300;文青攝影展海報，柔霧海邊奔跑的背影，頂端標題「夏日」&#12301;</sub></td>
</tr>
</table>

### Street in the Mirror

<table>
<tr>
<td width="25%" valign="top"><img src="examples/street_in_the_mirror_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a shop window stacking three layers of reflections, the photographer’s shadow among them&rdquo;</i><br>&#12300;櫥窗疊映著三層街景，拍攝者的影子也落在其中&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/street_in_the_mirror_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a lamp post growing precisely out of a passer-by’s head&rdquo;</i><br>&#12300;一根電線桿不偏不倚從路人頭頂長出來&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/street_in_the_mirror_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a street-photography exhibition poster, layered reflections, slanted title “MIRROR”&rdquo;</i><br>&#12300;街拍攝影展海報，層層反射疊映的街景，斜置標題「MIRROR」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/street_in_the_mirror_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a B&W photobook poster, a face sliced by a window frame, title “REFLECT”&rdquo;</i><br>&#12300;黑白攝影集海報，被窗框切開的臉與反射，頂端標題「REFLECT」&#12301;</sub></td>
</tr>
</table>

### Pale Light Moments

<table>
<tr>
<td width="25%" valign="top"><img src="examples/pale_light_moments_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a single trembling dew drop about to fall from a bright backlit leaf&rdquo;</i><br>&#12300;逆光明亮的葉尖，一顆將墜未墜、微微顫動的露珠&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/pale_light_moments_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a child’s small hand lifted into pale, near-overexposed morning light&rdquo;</i><br>&#12300;一個孩子的小手，舉進蒼白到近乎過曝的晨光裡&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/pale_light_moments_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a high-key photobook poster, a dew drop in blown-out morning light, title “Faint Light”&rdquo;</i><br>&#12300;高調柔光攝影集海報，過曝晨光中的一顆露珠，底部淡字標題「微光」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/pale_light_moments_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a minimalist exhibition poster, a small hand in pale light, title “LIGHT”&rdquo;</i><br>&#12300;極簡影展海報，蒼白光裡的一隻小手，頂端細字標題「LIGHT」&#12301;</sub></td>
</tr>
</table>

### Everyday Punchline

<table>
<tr>
<td width="25%" valign="top"><img src="examples/everyday_punchline_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a passer-by caught in an accidentally absurd pose&rdquo;</i><br>&#12300;路人恰好被抓拍到一個湊巧荒謬的姿勢&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/everyday_punchline_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a dog and its owner side by side wearing the exact same expression&rdquo;</i><br>&#12300;一隻狗和主人並排，露出一模一樣的表情&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/everyday_punchline_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a humour-photography exhibition poster, an absurd coincidence, title “PUNCHLINE”&rdquo;</i><br>&#12300;幽默攝影展海報，一個荒謬巧合的瞬間，大字標題「PUNCHLINE」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/everyday_punchline_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a candid-life photobook poster, a dog and owner with matching faces, title “Everyday Punchline”&rdquo;</i><br>&#12300;生活抓拍集海報，狗與主人同款表情，頂端標題「日常笑點」&#12301;</sub></td>
</tr>
</table>

### Vivid Garden

<table>
<tr>
<td width="25%" valign="top"><img src="examples/vivid_garden_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a drowning-dense field of crimson and magenta blooms with goldfish gliding through&rdquo;</i><br>&#12300;濃到快要滿出來的緋紅與洋紅花海，金魚在其間穿游&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/vivid_garden_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a single red datura flower beaded with rain, saturated to the edge of too-much&rdquo;</i><br>&#12300;一朵沾滿雨珠的紅色曼陀羅，飽和到近乎過度&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/vivid_garden_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a contemporary art poster, a full-bleed saturated flower field with goldfish, bold title “VIVID”&rdquo;</i><br>&#12300;濃艷的當代藝術展海報，滿版飽和的花海與穿游的金魚，下方一條乾淨白色色帶放粗體標題「VIVID」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/vivid_garden_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a flower-photography poster, over-saturated peonies and a glowing goldfish bowl, title “BLOOM”&rdquo;</i><br>&#12300;花卉攝影展海報，過飽和盛開的牡丹與發亮的金魚缸，頂部乾淨留白處放簡潔標題「BLOOM」&#12301;</sub></td>
</tr>
</table>

### Playful Film

<table>
<tr>
<td width="25%" valign="top"><img src="examples/playful_film_photo1.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a kid mid-goofy-face leaping through a sunlit field, hair flying&rdquo;</i><br>&#12300;陽光田野裡扮著鬼臉、頭髮飛揚跳起來的小孩&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/playful_film_photo2.jpg" width="100%"><br><sub><code>photo</code> <i>&ldquo;a child laughing wide around a dripping popsicle&rdquo;</i><br>&#12300;一個孩子咬著滴下汁的冰棒，笑得合不攏嘴&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/playful_film_poster1.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a film-snapshot photobook poster, a kid leaping and pulling a face, title “PLAY”&rdquo;</i><br>&#12300;底片寫真集海報，跳躍扮鬼臉的孩子，手寫感標題「PLAY」&#12301;</sub></td>
<td width="25%" valign="top"><img src="examples/playful_film_poster2.jpg" width="100%"><br><sub><code>poster</code> <i>&ldquo;a summer photo-show poster, a child laughing with a popsicle, title “Summer”&rdquo;</i><br>&#12300;夏日寫真展海報，咬著冰棒大笑的孩子，頂端標題「夏」&#12301;</sub></td>
</tr>
</table>

## Requirements

1. A ComfyUI that can already run **Qwen-Image-2.1** (it provides `TextEncodeQwenImage21` and the
   UNet / CLIP / VAE loaders you use).
2. A running **PE-T2I rewriter** on an OpenAI-compatible `/v1/chat/completions` endpoint, serving
   `Qwen/Qwen-Image-2.1-PE-T2I` (any backend — vLLM, llama-server, LM Studio, ...; any weight
   format). Point the node's `endpoint` at it (default `http://127.0.0.1:8207`).

No Python dependencies to install.

## Install

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/pottokao-dotcom/ComfyUI-QwenImage-PhotoStyles
```

Or install from the ComfyUI Registry via ComfyUI Manager (search "Qwen-Image Photo Styles").

## Inputs / Outputs

**Inputs** — `prompt` (multiline), `style` (dropdown: `None` + 17 styles), `endpoint`, `seed`,
`temperature`; optional `model`, `timeout_s`, `system_prompt_path`.

**Outputs** — `prompt` (STRING), `negative` (STRING), `width` (INT), `height` (INT),
`wh_ratio` (STRING). `seed` also picks one of the style's mood sub-presets, so re-rolling it
varies the feeling.

## The 17 styles

Black Fury · Geometry of Light · Warm Documentary · White Leap · Corner Elegance · Cold Power ·
Hyper Chic East · Private Diary · Color Behind Glass · Frozen Film Still · Fairytale Giants ·
Soft Everyday Light · Street in the Mirror · Pale Light Moments · Everyday Punchline ·
Vivid Garden · Playful Film.

Each style sheet in `styles/*.txt` specifies, per style: **Look, Lens language, Light, Emotion,
People, Scene & props, Colour**, plus per-style negatives and — for film-look styles — a fixed
grain clause.

## Models (optional — a ready-made low-VRAM family pack)

This node only needs the **PE-T2I rewriter**; everything else is your own Qwen-Image-2.1 graph.
If you want a self-quantized set to run the whole thing, here are 4-bit builds — **NVFP4** for
NVIDIA (ComfyUI / vLLM) and **GGUF Q4** for Mac / low-VRAM (llama.cpp / ComfyUI-GGUF).
("Heretic" = an abliterated / decensored build.)

| Component | NVFP4 · NVIDIA (ComfyUI / vLLM) | GGUF Q4 · Mac (llama.cpp / ComfyUI-GGUF) |
|---|---|---|
| **PE-T2I rewriter** (this node calls) | [Qwen-Image-2.1-PE-T2I-Heretic-NVFP4](https://huggingface.co/pottokao/Qwen-Image-2.1-PE-T2I-Heretic-NVFP4) | [Qwen-Image-2.1-PE-T2I-Heretic-GGUF](https://huggingface.co/pottokao/Qwen-Image-2.1-PE-T2I-Heretic-GGUF) |
| **DiT** (image model) | [Qwen-Image-2.1-DiT-NVFP4-ComfyUI](https://huggingface.co/pottokao/Qwen-Image-2.1-DiT-NVFP4-ComfyUI) | [Qwen-Image-2.1-DiT-GGUF](https://huggingface.co/pottokao/Qwen-Image-2.1-DiT-GGUF) |
| **Text encoder** (Qwen3-VL) | [Qwen-Image-2.1-Text-Encoder-Heretic-NVFP4](https://huggingface.co/pottokao/Qwen-Image-2.1-Text-Encoder-Heretic-NVFP4) | [Qwen-Image-2.1-Text-Encoder-Heretic-GGUF](https://huggingface.co/pottokao/Qwen-Image-2.1-Text-Encoder-Heretic-GGUF) |

The Qwen3-VL text-encoder **GGUF** needs this add-on in ComfyUI (fixes the 12288 shape error):
https://github.com/pottokao-dotcom/ComfyUI-GGUF-Qwen3VL-TE

## Example

See `example_workflow_api.json` (API format — enable *Dev mode* in ComfyUI settings, then
*Load (API Format)*). The loader nodes and model file names there are just an example; swap in
whatever Qwen-Image-2.1 models and format you use.

## Licensing

- Node code, style sheets, `presets.json`, docs — **MIT** (see `LICENSE`).
- `style_sp_plus.txt` is adapted from Qwen's official Qwen-Image-2.1-PE-T2I system prompt and
  remains under the **Qwen Research License** (see `NOTICE`). Review it before commercial use.
