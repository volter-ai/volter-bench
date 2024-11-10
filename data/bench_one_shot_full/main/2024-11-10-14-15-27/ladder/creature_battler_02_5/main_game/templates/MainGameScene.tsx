import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Swords, User, Bot } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
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

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Top HUD */}
      <nav className="flex justify-between items-center p-4 bg-secondary">
        <div className="flex items-center gap-2">
          <User className="h-5 w-5" />
          <span>{props.data.entities.player?.display_name}</span>
        </div>
        <Swords className="h-6 w-6" />
        <div className="flex items-center gap-2">
          <span>{props.data.entities.bot?.display_name}</span>
          <Bot className="h-5 w-5" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-12 py-6">
        {playerCreature && (
          <div className="relative">
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              className="transform scale-110"
            />
            <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
              Player
            </div>
          </div>
        )}

        {botCreature && (
          <div className="relative">
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              className="transform scale-110"
            />
            <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
              Opponent
            </div>
          </div>
        )}
      </div>

      {/* Action UI */}
      <div className="h-[30%] bg-card p-4 border-t">
        <div className="grid grid-cols-2 gap-4 h-full">
          {playerCreature?.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
