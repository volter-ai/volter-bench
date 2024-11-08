import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
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

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* Top HUD */}
      <nav className="w-full p-4 bg-secondary">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Sword className="h-5 w-5" />
            <span>Battle Scene</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
          </div>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-8 py-4">
        {playerCreature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Your Creature
            </div>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl="/placeholder.png"
            />
          </div>
        )}

        {botCreature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
              Opponent's Creature
            </div>
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              hp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl="/placeholder.png"
            />
          </div>
        )}
      </div>

      {/* Bottom UI */}
      <div className="w-full p-4 bg-secondary/50">
        <div className="flex flex-wrap gap-2 justify-center">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
