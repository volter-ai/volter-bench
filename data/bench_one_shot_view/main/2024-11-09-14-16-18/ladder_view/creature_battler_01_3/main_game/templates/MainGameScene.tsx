import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
    foe: Player
    player_creature: Creature
    foe_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const foeCreature = props.data.entities.foe_creature

  return (
    <div className="h-screen w-full flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-16 border-b flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Shield className="w-6 h-6" />
          <span>Player</span>
        </div>
        <div className="flex items-center gap-2">
          <Swords className="w-6 h-6" />
          <span>Battle Scene</span>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8">
        {playerCreature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold">Your Creature</span>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/creatures/${playerCreature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}

        {foeCreature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold">Opponent's Creature</span>
            <CreatureCard
              uid={foeCreature.uid}
              name={foeCreature.display_name}
              hp={foeCreature.stats.hp}
              maxHp={foeCreature.stats.max_hp}
              imageUrl={`/creatures/${foeCreature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}
      </div>

      {/* Skills/UI Region */}
      <div className="h-1/3 border-t bg-muted/50 p-4">
        <div className="grid grid-cols-4 gap-4">
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
