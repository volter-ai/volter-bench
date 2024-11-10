import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

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

  const { player, bot, player_creature, bot_creature } = props.data.entities

  if (!player || !bot || !player_creature || !bot_creature) {
    return null
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  const skills = player_creature.collections?.skills || []

  return (
    <div className="h-screen w-full flex flex-col">
      {/* HUD */}
      <nav className="h-16 bg-primary/10 flex items-center px-4 justify-between">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/default-player.png"
          />
        </div>
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4" />
          <span>Battle Scene</span>
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl="/default-bot.png"
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between px-8 gap-8">
        <div className="flex flex-col items-center gap-2">
          <span className="text-sm font-bold">Your Creature</span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl="/default-creature.png"
          />
        </div>

        <div className="flex flex-col items-center gap-2">
          <span className="text-sm font-bold">Opponent's Creature</span>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl="/default-creature.png"
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="min-h-[200px] bg-secondary/10 p-4">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {skills.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => handleSkillClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
