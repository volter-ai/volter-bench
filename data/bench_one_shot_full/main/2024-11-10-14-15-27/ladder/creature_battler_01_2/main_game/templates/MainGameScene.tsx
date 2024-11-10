import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    damage: number
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
    player_creature: Creature
    bot_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, bot, player_creature, bot_creature } = props.data?.entities || {}

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    // Map skill UID to button slug format
    const buttonSlug = `skill_${skillUid}`
    if (availableButtonSlugs.includes(buttonSlug)) {
      emitButtonClick(buttonSlug)
    }
  }

  const skills = player_creature.collections?.skills || []

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <nav className="w-full bg-secondary p-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/placeholder-player.png"
          />
        </div>
        <Swords className="w-6 h-6" />
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl="/placeholder-opponent.png"
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-8 py-4">
        <div className="flex flex-col items-center gap-4">
          <span className="text-sm font-bold">Your Creature</span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl="/placeholder-creature.png"
          />
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-sm font-bold">Opponent</span>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl="/placeholder-creature.png"
          />
        </div>
      </div>

      {/* Skills UI */}
      <div className="bg-secondary/50 p-4 min-h-[200px]">
        <div className="flex flex-wrap justify-center gap-2">
          {skills.length > 0 ? (
            skills.map((skill) => {
              const buttonSlug = `skill_${skill.uid}`
              return (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  name={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  disabled={!availableButtonSlugs.includes(buttonSlug)}
                  onClick={() => handleSkillClick(skill.uid)}
                />
              )
            })
          ) : (
            <div className="text-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
