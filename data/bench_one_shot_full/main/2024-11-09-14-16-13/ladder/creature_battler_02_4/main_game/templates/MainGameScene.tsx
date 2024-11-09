import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
    [key: string]: any
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
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
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature

  return (
    <div className="h-screen w-full flex flex-col bg-background">
      {/* Top HUD */}
      <nav className="h-[10vh] flex items-center justify-between px-6 border-b">
        {props.data.entities.player && (
          <PlayerCard
            uid={props.data.entities.player.uid}
            name={props.data.entities.player.display_name}
          />
        )}
        {props.data.entities.opponent && (
          <PlayerCard
            uid={props.data.entities.opponent.uid}
            name={props.data.entities.opponent.display_name}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="h-[50vh] flex items-center justify-between px-12">
        <div className="flex flex-col items-center gap-4">
          <Shield className="h-8 w-8 text-blue-500" />
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        <div className="flex flex-col items-center gap-4">
          <Swords className="h-8 w-8 text-red-500" />
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* Bottom UI */}
      <div className="h-[40vh] bg-muted p-6 flex flex-col gap-4">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={skill.stats}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
