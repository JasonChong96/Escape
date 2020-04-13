# The script of the game goes in this file.

# Sorry for the mess but it works.

define e = Character("Eileen")



init:
    $ config.rollback_enabled = False
    $ config.keymap['skip'].clear()
    $ config.keymap['game_menu'].clear()
    $ screen_center = Position(xpos=0.2, ypos=0.2)
    define m = Character('Man', color="#c8c8ff")
    define f = Character('Woman', color="#c8c8ff")
    define narratorz = Character('Narrator', color="#c8c8ff")
    define nameless_nvl = Character('', kind=nvl, color="#c8c8ff", what_text_align=0.5, what_xalign=0.5, what_yalign=0.2)
    define rat = Character('Russell', color="#c8c8ff")

init python:
    import time
    dirt_actions_left = -1
    pee_actions_left = -1
    currentuser = ""
    try:
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
            if user:
                currentuser = user
    except:
        pass

    # Create an object to store the last time playtime was updated.
    # Since we create it in init, it won't be saved or participate
    # in rollback.
    playtime = object()
    playtime.last_update = time.time()

    # Store the total playtime in persistent.total_playtime.
    if persistent.total_playtime is None:
        persistent.total_playtime = 0

    # This is called periodically (several times a second) to update
    # persistent.total_playtime.
    def playtime_callback():
        now = time.time()
        delta = now - playtime.last_update
        persistent.total_playtime += delta
        playtime.last_update = now

    config.periodic_callbacks.append(playtime_callback)
    def clear_data():
        persistent._clear(progress=True)
        persistent.total_playtime = 0

    def get_playtime():
        seconds = persistent.total_playtime
        minutes, seconds = int(seconds // 60), int(seconds % 60)
        return str(minutes) + " minutes " + str(seconds) + " seconds"

    def dirt_check():
        global dirt_actions_left
        if dirt_actions_left < 0:
            return
        dirt_actions_left -= 1
        if dirt_actions_left == 3:
            renpy.say(None, "(Footsteps slowly approaching...)")
            renpy.say(None, "Oh no! Are they following my dirt trail?")
        elif dirt_actions_left <= 0:
            renpy.say(None, "Oh no! Someone followed my dirt trail!")
            renpy.jump('caught')

    def pee_check():
        global pee_actions_left
        if pee_actions_left < 0:
            return
        pee_actions_left -= 1
        if pee_actions_left <= 0:
            renpy.say(None, "Oh my, I need to pee. It must be the water I drank just now…")
            renpy.jump('caught')

    def ingame_clock_move():
        if not persistent.living_room_front_door_discovered:
            return
        if persistent.num_ground_floor_actions is None:
            persistent.num_ground_floor_actions = 0
        persistent.num_ground_floor_actions += 1
        if persistent.num_ground_floor_actions >= 15 and not persistent.living_room_front_door_unlocked:
            renpy.call('front_door_open')

    def action_taken():
        mtt.TextAction("").__call__()
        if persistent.living_room_front_door_unlocked:
            return
        dirt_check()
        pee_check()
        ingame_clock_move()
        renpy.sound.stop()

    def get_in_game_clock_time():
        action_count = persistent.num_ground_floor_actions
        if action_count is None:
            action_count = 0

        if action_count < 3:
            minutes_clock = str(45 + action_count * 5)
            while len(minutes_clock) < 2:
                minutes_clock = '0' + minutes_clock
            return '5:' + str(45 + action_count * 5)
        elif action_count < 15:
            minutes_clock = str((action_count - 3) * 5)
            while len(minutes_clock) < 2:
                minutes_clock = '0' + minutes_clock
            return '6:' + str((action_count - 3) * 5)
        else:
            return '7:00'

    def ground_floor_action_taken():
        pass
# The game starts here.

label start:
    define self = Character(currentuser, color="#c8c8ff")

    image babyroom = im.Scale("bg babyroom.png", 1920, 1080)
    image bg attic = im.Scale("bg attic.png", 1920, 1080)
    image attic_curtains = im.Scale("attic curtains.png", 1920, 1080)
    image baygon = im.Scale("baygon.png", 300, 300)
    image poison_floor = im.FactorScale("poison.png", 0.5, 0.5)
    image bg balcony = im.Scale("bg balcony.png", 1920, 1080)
    image bg toilet = im.Scale("bg toilet.png", 1920, 1080)
    image bg stairs = im.Scale("bg stairs.png", 1920, 1080)
    image bg stairs dog = im.Scale("bg stairs dog.png", 1920, 1080)
    image bg dogroom = im.Scale("bg dogroom.png", 1920, 1080)
    image bg wardrobe = im.Scale("bg wardrobe.png", 1920, 1080)
    image bg dining room = im.Scale("bg dining room.png", 1920, 1080)
    image bg master bedroom = im.Scale("bg master bedroom.png", 1920, 1080)
    image bg living room = im.Scale("bg living room.png", 1920, 1080)
    image bg hallway ground = im.Scale("bg hallway ground.png", 1920, 1080)
    image bg hallway = im.Scale("bg hallway.png", 1920, 1080)
    image bg kitchen = im.Scale("bg kitchen.png", 1920, 1080)
    image bg ending = im.Scale("bg ending.png", 1920, 1080)
    image bg ending1 = im.Scale("bg ending 1.png", 1920, 1080)
    image bg ending caught = im.Scale("bg ending caught.png", 1920, 1080)
    image bg outside = im.Scale("bg outside.png", 1920, 1080)
    image dog toy = im.FactorScale("dog toy.png", 0.075, 0.075)
    image poop = im.FactorScale("poop.png", 1, 1)
    image dog2 = im.FactorScale("dog2.png", 1, 1)
    image ending door = im.FactorScale("ending door.png", 0.5)

    image caught = "caught.png"
    image babyroom_food = "babyroom food.png"
    python:
        if persistent.eaten is None:
            persistent.eaten = set()
        if persistent.num_caught is None:
            persistent.num_caught = 0
    nameless_nvl """
    Looks like the coast is clear….
    """
    play sound "audio/slow footsteps.ogg"
    nameless_nvl "Oh no, I hear them coming."
    nameless_nvl "I cannot get caught again... better get moving, NOW!"
    nvl clear
    # "Oh no, oh no, oh no. They know I’m here. "
    play music "audio/bgm.ogg"
    "You are stuck in this house, and your objective is to get out."
    "There are items along the way that you can interact with to help you on your journey. Try not to get caught!"
    jump toilet

    label babyroom:
        scene babyroom with fade
        stop sound fadeout 1.0
        show babyroom
        $ action_taken()
        $ persistent.babyroom_entered = True
        call screen babyroom_options(not persistent.babyroom_ate_food, persistent.hallway_entered)
        if _return == 'babyroom.toys':
            $ persistent.babyroom_can_exit = True
            if persistent.babyroom_played_with_toys:
                menu:
                    "Hold up. I’ve seen these before. Should I examine them again?"
                    "Yes":
                        pass
                    "No":
                        "Yeah, not such a good idea huh? Let’s get back to escaping."
                        jump babyroom
            $ persistent.babyroom_played_with_toys = True
            play sound "audio/babyroom rummage.ogg"
            "*Rummaging through the toys.*"
            "Oooh, what’s this?"
            "Oh no."
            "No wait. No, no, no!"
            jump caught
        elif _return == 'babyroom.food':
            $ persistent.babyroom_can_exit = True
            $ persistent.babyroom_ate_food = True
            $ persistent.eaten.add('babyroom')
            "*Eating spilled food*"
            play sound "audio/door open.ogg"
            "Ooooh myyy that tastes so yummy!"
            scene black with dissolve
            show caught at top
            "You got caught!"
            "But wait… what! Argh, not again! I can’t believe I got distracted that quickly…"
            $ persistent.num_caught += 1
            return
        elif _return == 'babyroom.cot':
            $ persistent.babyroom_can_exit = True
            if persistent.babyroom_hidden_in_cot:
                "*Hides under the baby cot*"
                "Looks the same as last time..."
            else:
                $ persistent.babyroom_hidden_in_cot = True
                "*Hides under the baby cot*"
                play sound "audio/door open.ogg"
                "Someone’s in here, they are looking for me."
                play sound "audio/door close.ogg"
                "..."
                "Thank goodness they’re gone now. I need to leave now."
            jump babyroom
        elif _return == 'babyroom.exit':
            jump hallway

    label attic:
        scene bg attic with fade
        if not persistent.attic_entered:
            "It’s so dark and musky here… I recognise this room, it’s the attic, but a lot dustier than I remember."
        $ persistent.attic_entered = True
        $ action_taken()
        call screen attic_options(persistent.balcony_entered, persistent.dog_room_entered)
        if _return == 'attic.curtains':
            "*looking behind the curtains*"
            "This house has three storeys. I have to escape from the front door in the living room."
            jump attic
        elif _return == 'attic.photos':
            show attic photo 1 at top with dissolve
            "*Investigating the photo frame*"
            "These people. Thinking of them makes me shudder. But this child, he looks very familiar, and is quite cute I must say."
            show attic photo 2 at top with dissolve
            "Oh what monsters!"
            jump attic
        elif _return == 'attic.blanket':
            jump hallway
        elif _return == 'attic.dogroom':
            jump dogroom
        elif _return == 'attic.balcony':
            jump balcony
        else:
            jump attic

    label balcony:
        scene bg balcony with fade
        play sound "audio/balcony wind.ogg"
        if not persistent.balcony_entered:
            "Oh! What a refreshing breeze!"
            "This balcony provides quite a lovely view as well, but yes, I need to focus."
        $ action_taken()
        $ persistent.balcony_entered = True
        call screen balcony_options()
        if _return == 'balcony.plants':
            "*Investigates the flower pot*"
            "There’s nothing here... But ew, all the soil is making my legs dirty. I’m leaving a trail!!!"
            if dirt_actions_left < 0:
                $ dirt_actions_left = 7
            jump balcony
        elif _return == 'balcony.baygon':
            "*Examines the can behind the flower pot*"
            "What’s that smell? Oh another friend! But, he’s not moving…"
            "Oh, he’s…. dead?! What is going on here with this family."
            jump balcony
        elif _return == 'balcony.attic':
            jump attic
        else:
            jump balcony

    label hallway:
        scene bg hallway with fade
        $ action_taken()
        $ persistent.hallway_entered = True
        call screen hallway_options(persistent.wardrobe_entered,
                                    persistent.master_bedroom_entered,
                                    persistent.babyroom_entered,
                                    persistent.toilet_entered,
                                    persistent.attic_entered)
        if _return == 'hallway.wardrobe':
            play sound "audio/door open.ogg"
            jump wardrobe
        elif _return == 'hallway.master_bedroom':
            play sound "audio/door open.ogg"
            jump master_bedroom
        elif _return == 'hallway.babyroom':
            play sound "audio/door open.ogg"
            jump babyroom
        elif _return == 'hallway.toilet':
            play sound "audio/door open.ogg"
            jump toilet
        elif _return == 'hallway.stairs':
            jump stairs
        elif _return == "hallway.attic":
            jump attic
        else:
            jump hallway

    label stairs:
        $ action_taken()
        $ persistent.stairs_entered = True
        if persistent.hallway_ground_entered:
            jump hallway_ground
        elif persistent.dog_room_toy_examined:
            scene bg stairs with fade
            menu:
                "Head down?"
                "Yes":
                    jump hallway_ground
                "No":
                    jump hallway
        else:
            scene bg stairs dog with fade
            "*Peering down the staircase*"
            play sound 'audio/dog snoring.ogg'
            "It’s the monster again. Its beady eyes and saggy skin creeps me out."
            "I remember the last time he hurt me. There must be a way to get around him…"
            jump hallway


    label toilet:
        scene bg toilet with fade
        if persistent.dog_room_toy_examined and not persistent.hallway_ground_entered:
            "The monster is in it's den now, maybe I can head downstairs!"
        $ action_taken()
        $ persistent.toilet_entered = True
        call screen toilet_options(not persistent.knows_rat and not persistent.is_rat_dead)
        if _return == 'toilet.mirror':
            "The mirror is too high up and I can’t reach it. :("
            "But I really really really need to leave this place!!!"
            jump toilet
        elif _return == 'toilet.puddle':
            play sound "audio/toilet puddle 1.ogg"
            "UGH, I HATE WATER."
            if dirt_actions_left >= 0:
                "Hey the dirt trail stopped!"
                $ dirt_actions_left = -1
            jump toilet
        elif _return == 'toilet.poison':
            if persistent.toilet_ate_poison:
                menu:
                    "This brings back horrible memories. But should I at least investigate it again?"
                    "Yes":
                        scene black with dissolve
                        show caught at top
                        "Wait, no, what?"
                        "How did I not hear him come in? I have failed myself, yet again."
                        $ persistent.num_caught += 1
                        return
                    "No":
                        "Looks like a bottle from hell anyways..."
                        jump toilet
            "*looking at item*"
            "This looks interesting. I wonder how it tastes like?"
            scene black with dissolve
            show caught at top
            "Wait, no, what?"
            "How did I not hear him come in? I have failed myself, yet again."
            $ persistent.toilet_ate_poison = True
            $ persistent.num_caught += 1
            return
        elif _return == 'toilet.hallway':
            jump hallway
        elif _return == 'toilet.rat':
            play sound "audio/rat squeaking.ogg"
            rat "Hello [currentuser]. The name’s Russell. And I have terrible news for you: You NEED to get out of here!"
            self "Huh? You have the guts to come out here in the open in front of me."
            play sound "audio/rat squeaking.ogg"
            rat "They are out to get you. You MUST leave."
            self "And why would I trust YOU of all animals?"
            play sound "audio/rat squeaking.ogg"
            rat "Please just trust me. I need to hide now. Good luck pal!"
            "What was that about? He doesn’t seem evil. Maybe I should take his advice..."
            $ persistent.knows_rat = True
            jump toilet
        else:
            jump toilet

    label dogroom:
        scene bg dogroom with fade
        $ action_taken()
        if not persistent.dog_room_entered:
            "Judging from the smell, I believe this is where the monsters live."
        if persistent.dog_room_toy_examined:
            "Wait... The monster is sleeping in here, time to get out."
            jump attic
        $ persistent.dog_room_entered = True
        call screen dogroom_options(persistent.stairs_entered)
        if _return == 'dogroom.attic':
            jump attic
        elif _return == 'dogroom.poop':
            show poop at Position(xpos=0.5, ypos=0.5)
            "*Examining brown thing on the floor*"
            "Ooh it seems moist, better not touch it. But it sure looks interesting."
            jump dogroom
        elif _return == "dogroom.toy":
            play sound "audio/dogroom toy.ogg"
            "..."
            play sound "audio/dog growl.ogg"
            "..."
            menu:
                "Oh no, the monster is awake! HIDE! NOW!"
                # "Hide in cupboard":
                #     scene black with dissolve
                #     "*Hiding in the cupboard*"
                #     "HAH. Nice try you beast. I won’t let you get me this time!"
                #     "Ah, I see you have fallen asleep again. Now’s the time to sneak out!"
                #     menu:
                #         "Sneak out of the Monster’s Den and back to Hallway":
                #             $ persistent.dog_room_toy_examined = True
                #             jump hallway
                "Hide behind monster's bed":
                    "*Not so inconspicuously hiding behind dog bed*"
                    play sound "audio/dog barking.ogg"
                    "..."
                    scene black with dissolve
                    "Oh no he can still see me? Help, help!"
                    $ persistent.dog_room_toy_examined = True
                    jump caught

        jump dogroom
    label wardrobe:
        scene bg wardrobe with fade
        if not persistent.wardrobe_entered:
            "Wow where is this place? I’ve never been here before. So glittery and shiny!"
        if persistent.wardrobe_clothes_caught and persistent.wardrobe_jewellery_looked and persistent.wardrobe_shoes_examined:
            "This wardrobe is a dangerous place... Wardrobe? More like Warzone."
        $ action_taken()
        $ persistent.wardrobe_entered = True
        call screen wardrobe_options(not persistent.wardrobe_jewellery_looked)
        if _return == 'wardrobe.master_bedroom':
            jump master_bedroom
        elif _return == 'wardrobe.hallway':
            jump hallway
        elif _return == 'wardrobe.shoes':
            if persistent.wardrobe_shoes_examined:
                "Okay, these towers of hell are fragile. FRAGILE. I need to handle them with care."
                menu:
                    "Take a look at them?"
                    "Yes":
                        play sound "audio/wardrobe shoe.ogg"
                        "Wonderful. Simply wonderful..."
                        scene black with dissolve
                        show caught at top
                        "You got caught!"
                        "Why am I so careless?"
                        $ persistent.num_caught += 1
                        return
                    "No":
                        "Like I said, they are fragile. Maybe I’m better off leaving them alone."
                        jump wardrobe
            else:
                "Who has such big feet?"
                "And why do you even need so many shoes for two foots-"
                "*trips*"
                play sound "audio/wardrobe shoe.ogg"
                "No-"
                scene black with dissolve
                show caught at top
                "You got caught!"
                "Why am I so careless?"
                $ persistent.wardrobe_shoes_examined = True
                $ persistent.num_caught += 1
                return
        elif _return == 'wardrobe.ring':
            if persistent.wardrobe_jewellery_looked:
                menu:
                    "Oooo shiny… something as beautiful as this could just be tasty as well… Taste it?"
                    "Yes":
                        play sound "audio/fast footsteps.mp3"
                        "Taste like... nothing?"
                        "Wait what's that?"
                        scene black with dissolve
                        show caught at top
                        "You got caught!"
                        $ persistent.wardrobe_jewellery_looked = True
                        "What... How did they know I’m here? No, no, NO! LET ME GO!"
                        $ persistent.num_caught += 1
                        return
                    "No":
                        "On second thought, maybe it’s not such a good idea. "
                        jump wardrobe
            else:
                "*There was something sparkling in the distance*"
                "It’s very shiny… What am I supposed to do with this?"
                play sound "audio/fast footsteps.mp3"
                "I guess anything can be eaten."
                scene black with dissolve
                show caught at top
                "You got caught!"
                $ persistent.wardrobe_jewellery_looked = True
                "What... How did they know I’m here? No, no, NO! LET ME GO!"
                $ persistent.num_caught += 1
                return
        elif _return == 'wardrobe.clothes':
            if persistent.wardrobe_clothes_caught:
                menu:
                    "Not sure why just looking at it feels traumatic... Should I brave it again?"
                    "Yes":
                        "Oh no. That traumatic feeling is back. I’M TRAPPED! HELP!"
                        scene black with dissolve
                        show caught at top
                        "You got caught!"
                        $ persistent.wardrobe_clothes_caught = True
                        "I made too much noise out of panic. I must be quiet if I want to escape."
                        $ persistent.num_caught += 1
                        return
                    "No":
                        "Yeah, doesn’t look like such a good idea either. Now, back to escaping."
                        jump wardrobe
            else:
                "*large piles loomed above me*"
                scene black with dissolve
                "First of all, the smell is… is… so good."
                "But I can’t seem to find my way out of here?"
                "Erm, help? HELP!"
                scene black with dissolve
                show caught at top
                "You got caught!"
                $ persistent.wardrobe_clothes_caught = True
                "I made too much noise out of panic. I must be quiet if I want to escape."
                $ persistent.num_caught += 1
                return
        jump wardrobe

    label master_bedroom:
        scene bg master bedroom with fade
        $ action_taken()
        if not persistent.master_bedroom_entered:
            "Ah, I have arrived at the Humans’ Den."
        $ persistent.master_bedroom_entered = True
        call screen master_bedroom_options(persistent.master_bedroom_other_door_entered)
        if _return == 'master_bedroom.hallway':
            jump hallway
        elif _return == 'master_bedroom.wardrobe':
            $ persistent.master_bedroom_other_door_entered = True
            jump wardrobe
        elif _return == 'master_bedroom.socket':
            if persistent.master_bedroom_socket_touched:
                menu:
                    "Hold up. This reminds me of someone or something yanking me aggressively. But I didn’t get a close look last time… Why not give it a go?"
                    "Yes":
                        pass
                    "No":
                        "It actually does look dangerous, does it?"
                        jump master_bedroom
            play sound "audio/fast footsteps.mp3"
            "*Reaching for the power socket*"
            scene black with dissolve
            show caught at top
            "You got caught!"
            "That was such an unnecessarily hard yank!"
            "The humans pulled me away so aggressively???"
            "I don’t understand, but I need to think of a new plan this time..."
            $ persistent.master_bedroom_socket_touched = True
            $ persistent.num_caught += 1
            return
        elif _return == 'master_bedroom.lamp':
            if 'candy' in persistent.eaten:
                show master bedroom lamp at top
                "Nice lamp."
            else:
                "What is this under the lamp?"
                show candy at top
                "It smells sweet and good. Let me taste it…"
                "..."
                "*Eating*"
                "Mmm! Better than the same old food they feed me everyday"
                $ persistent.eaten.add('candy')
        elif _return == 'master_bedroom.roomba':
            if persistent.master_bedroom_roomba_examined:
                menu:
                    "Wait. I know this thing. It makes a really loud sound. Maybe if I am extra careful this time, it wouldn’t?"
                    "Examine it":
                        pass
                    "Nevermind":
                        "Yeah. Let’s leave it and go back to escaping."
                        jump master_bedroom
            $ persistent.master_bedroom_roomba_examined = True
            "*Examining circular thingamaji on the floor*"
            play sound "audio/master bedroom vacuum.ogg"
            menu:
                "Erk what’s this noise? Quick quick, what do i do now?"
                "Hide under bed":
                    scene black with dissolve
                    "*Hiding under the bed*"
                    play sound "audio/slow footsteps.ogg"
                    "..."
                    "How does it know my favourite hiding spot! HELP IT’S COMING"
                    scene black with dissolve
                    show caught at top
                    'You got caught!'
                    "Oh well… It seems the humans are smarter than the monsters..."
                    $ persistent.num_caught += 1
                    return
                "Go back to hallway":
                    scene bg hallway with fade
                    "*Rushing into the hallway*"
                    scene black with dissolve
                    show caught at top
                    'You got caught!'
                    "I. Am. An. Idiot. Sandwich. How did I get caught again…."
                    $ persistent.num_caught += 1
                    return
                "Enter the other door" if not persistent.master_bedroom_other_door_entered:
                    $ persistent.master_bedroom_other_door_entered = True
                    scene bg wardrobe with fade
                    "*Panting very hard*"
                    "It seems safe in here… for now… "
                    jump wardrobe
                "Enter the wardrobe" if persistent.master_bedroom_other_door_entered:
                    scene bg wardrobe with fade
                    "*Panting very hard*"
                    "It seems safe in here… for now… "
                    jump wardrobe
        jump master_bedroom

    label hallway_ground:
        $ ground_floor_action_taken()
        scene black with fade
        $ action_taken()
        if not persistent.hallway_ground_entered:
            "Made it to the first floor. I can almost taste the freedom!"
        $ persistent.hallway_ground_entered = True
        show bg hallway
        call screen hallway_ground_options(persistent.kitchen_entered, persistent.dining_room_entered, persistent.living_room_entered, persistent.is_rat_dead, persistent.knows_rat)
        if _return == "hallway_ground.kitchen":
            if persistent.living_room_front_door_unlocked:
                "Wait... The monster is in there."
                jump hallway_ground
            else:
                jump kitchen
        elif _return == "hallway_ground.dining_room":
            jump dining_room
        elif _return == "hallway_ground.living_room":
            jump living_room
        elif _return == "hallway_ground.hallway":
            jump hallway
        elif _return == "hallway_ground.rat":
            if not persistent.is_rat_dead and persistent.knows_rat:
                "It’s that rat from before… isn’t he supposed to be hiding? Let’s go ask him."
                self "Psst! Hey Russell! What are you doing here? Aren’t you supposed to be hiding?"
                rat "Shhh! I got hungry so I came out. What are you still doing here? Get out of here NOW!"
                play sound "audio/fast footsteps.mp3"
                "Wait. What was that?"
                scene black with fade
                show caught at top
                "You got CAUGHT!"
                show live rat at top
                "Oh dear..."
                $ persistent.is_rat_dead = True
                $ persistent.num_caught += 1
                return
            elif not persistent.is_rat_dead and not persistent.knows_rat:
                "It’s that rat from before… isn’t he supposed to be hiding? Let’s go ask him."
                self "Psst! Hey hey!"
                rat "Shhh! Are you trying to get me killed? Who are you anyway?"
                play sound "audio/fast footsteps.mp3"
                "I just wanna ask how can I… oh no..."
                scene black with fade
                show caught at top
                "You got CAUGHT!"
                show live rat at top
                "What have I done..."
                $ persistent.is_rat_dead = True
                $ persistent.num_caught += 1
                return
            else:
                "It’s that rat from before… isn’t he supposed to be hiding? Let’s go ask him."
                "Psst! Hey hey!"
                "..."
                "Ohno, he's cold and not moving..."
                jump hallway_ground
        elif _return == 'hallway_ground.clock':
            $ clock_time_to_show = get_in_game_clock_time()
            "It is currently [clock_time_to_show]. Something's going to happen soon, I can feel it."
            if not (persistent.num_ground_floor_actions is None) and persistent.num_ground_floor_actions > 0 and persistent.num_ground_floor_actions < 15:
                $ persistent.num_ground_floor_actions -= 1
            jump hallway_ground

    label dining_room:
        $ ground_floor_action_taken()
        scene bg dining room with fade
        if not persistent.dining_room_entered:
            "Woah, something here smells really good… I wonder what it is…?"
        $ action_taken()
        $ persistent.dining_room_entered = True
        $ fresh_eaten = 'dining.fresh' in persistent.eaten
        call screen dining_room_options(not persistent.dining_room_leftover_eaten, not fresh_eaten)
        if _return == 'dining_room.hallway':
            jump hallway_ground
        elif _return == 'dining_room.cutlery':
            if persistent.dining_room_cutlery_knocked:
                menu:
                    "A loud sound rings in my ears. Didn’t get a close look last time, let me try again."
                    "Yes":
                        "Not again! Sigh..."
                    "No":
                        "Maybe not, it looks really unstable."
                        jump dining_room
            else:
                $ persistent.dining_room_cutlery_knocked = True
                "*Examining cutlery on the table*"
            play sound "audio/dining room cutlery.ogg"
            "*Loud clang*"
            "Oh sh*t. Why am I so clumsy!"
            scene black with dissolve
            show caught at top
            "You got caught!"
            "Not again! Sigh..."
            $ persistent.num_caught += 1
            return
        elif _return == 'dining_room.leftovers':
            if persistent.dining_room_leftover_eaten:
                "*Shudders*"
                "Better not try that again."
            else:
                $ persistent.dining_room_leftover_eaten = True
                $ persistent.eaten.add('dining.leftovers')
                play sound "audio/dining room eating.ogg"
                "*Eating leftover food*"
                scene black with dissolve
                show caught at top
                "You got caught!"
                "Huh? What? Argh, it’s always me greed that kills me…."
                $ persistent.num_caught += 1
                return
        elif _return == 'dining_room.food':
            "*Eating freshly cooked food*"
            $ persistent.eaten.add('dining.fresh')
            play sound "audio/dining room eating.ogg"
            "Mmm yummy. This is really delicious...."
        elif _return == 'dining_room.cockroaches':
            scene black with dissolve
            "*Crawling under the dining table*"
            "OMG, what are these things? I think I heard the humans talk about them before… "
            "Cockroaches… but they are… dead?! RIP friends, I’mma get out of here. "
        jump dining_room

    label kitchen:
        $ ground_floor_action_taken()
        if persistent.living_room_front_door_unlocked:
            jump hallway_ground
        scene bg kitchen with fade
        if not persistent.kitchen_entered:
            "You entered the Kitchen… or shall we say HEAVEN?"
        $ action_taken()
        $ persistent.kitchen_entered = True
        call screen kitchen_options()
        if _return == "kitchen.hallway":
            jump hallway_ground
        elif _return == "kitchen.water":
            show water at top
            menu:
                "I could use some water after all that exploring."
                "Drink Water":
                    "*Drinks some water*"
                    "Thirst quenching! Now, where was I?"
                    if pee_actions_left < 0:
                        $ pee_actions_left = 2
                    jump kitchen
                "Forget it":
                    "My thirst is quenched… and I really don’t want to pee my pants anymore."
                    jump kitchen
        elif _return == 'kitchen.dishes':
            "*Crawls up to the sink*"
            show dirtydishes at top
            "Just stacks and stacks of dirty dishes. Does this family even clean after themselves?"
            "Horrible… but I like it."
        elif _return == "kitchen.trashcan":
            scene black with dissolve
            "*Looking inside the trashcan*"
            "Wow, just wow. The darkness in here is fascinating."
        jump kitchen

    label living_room:
        scene bg living room with fade
        if not persistent.living_room_entered:
            "Wow this is a large room. That is a very big door, is it the door for me to get out?"
        $ persistent.living_room_entered = True
        if persistent.living_room_front_door_unlocked:
            scene black with fade
            "*Looking at the front door*"
            menu:
                "Is this… finally… it? Have I made it?"
                "ESCAPE":

                    jump ending
        else:
            "*Sneakily inch closer*"
            play sound "audio/dog snoring.ogg"
            show dog2 at Position(xpos=0.5, ypos=0.95)
            $ persistent.living_room_front_door_discovered = True
            "Argh, another monster. At this rate, I’m doomed to be stuck here, how do I even escape??"
            "I need to create a distraction."
            jump hallway_ground

    label ending:
        scene black with fade
        $ mtt.TextAction("").__call__()
        narratorz "Hello there, finally you’re almost out!"
        menu:
            narratorz "We’re just curious and we hope you’d share with us, in your honest opinion, who do you think you’re playing as?"
            "A rat escaping the house":
                "Checking results..."
            "The family's new cat":
                "Checking results..."
            "An unwanted cockroach":
                "Checking results..."
            "A trapped spirit":
                "Checking results..."
            "A baby trying to flee":
                "Checking results..."
            "A burglar attempting to leave unseen":
                "Checking results..."
        narratorz "It turns out 30\% of players agree with you!"
        narratorz "Now... let's find out the real answer."
        "*Moving closer to the door*"
        call screen ending_options()
        if _return == 'ending.door':
            if len(persistent.eaten) >= 4:
                jump ending_food_coma
            elif len(persistent.eaten) >= 2:
                jump ending_food_coma_2
            else:
                jump ending_true
        jump ending

    label ending_food_coma:
        show ending door at Position(xoffset=0, yoffset=-300)
        "I finally made it, it's time to escape!!!"
        "But I think I ate too much food along the way… The food coma is hitting me…"
        "I.. I need to… es... "
        scene black with fade
        f "Oh baby, you fell asleep at the doorstep! Playtime is over, it’s time for your shower."
        "Nooo.. Please don’t put me in the shower :("
        stop music
        scene bg ending caught with fade
        stop music
        stop sound
        $ timing = get_playtime()
        "Congratulations you took [timing] to reach the first ending! Your game will be reset"
        $ clear_data()
        return

    label ending_food_coma_2:
        scene bg ending1 # No fade intentional
        "I finally made it, it's time to escape!!!"
        stop music
        "Ah the great outdoors. The sun is warm and it’s making me sleepy..."
        "Did I eat too much along the way? Just a bit more… It’s no good, my eyes are closing…"
        "I shouldn’t have ate so much.."
        scene black with fade
        play sound "audio/slow footsteps.ogg"
        f "Oh baby, how did you open the door! You’re very smart but playtime is over, it’s time for your shower."
        "Nooo.. Please don’t put me in the shower :("
        scene bg ending caught with fade
        stop music
        stop sound
        $ timing = get_playtime()
        "Congratulations you took [timing] to reach the second ending! Your game will be reset"
        $ clear_data()
        return

    label ending_true:
        scene bg ending1
        "I’ve learnt from my past mistakes! I am full of energy and I will definitely escape this time…!"
        scene bg outside with fade
        "Ah ha! I’ve finally made it! I smell freedom. I hear the birds chirping in my success. I.. I..."
        play sound "audio/fast footsteps.mp3"
        "… hear footsteps?"
        f "Baby what are you doing outside the house?! Honey why did you let our baby out!"
        m "What no! I didn’t!"
        f "Oh baby, how did you open the door! You’re very smart but playtime is over, it’s time for your shower."
        scene black with fade
        "Nooo.. Please don’t put me in the shower :("
        stop music
        stop sound
        scene bg ending caught with fade
        $ timing = get_playtime()
        "Congratulations you took [timing] to reach the TRUE ending! Your game will be reset"
        $ clear_data()
        return


    label front_door_open:
        $ persistent.living_room_front_door_unlocked = True
        scene black with dissolve
        "Wait what? The entire house’s power went off. You hear a scream from the kitchen."
        f "Honey! What’s going on?!"
        m "Don’t worry! Just stay calm!"
        play sound "audio/dog barking.ogg"
        "*”Woof!” The monster woke up and ran to the kitchen.*"
        f "This is getting out of hand! Why is there a power outage at 7pm sharp every single night?!"
        menu:
            "Now’s the time to escape!"
            "Go back to living room":
                call ending from _call_ending
                $ MainMenu(confirm=False)()


    label caught:
        scene black
        with fade
        show caught at top
        "YOU GOT CAUGHT!"
        "Not so simple right? Try again."
        $ persistent.num_caught += 1
        $ MainMenu(confirm=False)()
    # This ends the game.

    return
