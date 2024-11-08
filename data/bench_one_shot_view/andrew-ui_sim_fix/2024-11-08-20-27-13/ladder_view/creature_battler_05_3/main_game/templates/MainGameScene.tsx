import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Sword, ArrowLeft } from 'lucide-react'
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
  }
  meta: {
    skill_type: string
    prototype_id: string
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
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  meta: {
    prototype_id: string
  }
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const player = props.data.entities.player
  const opponent = props.data.entities.opponent
  const playerCreature = player?.entities.active_creature
  const opponentCreature = opponent?.entities.active_creature

  if (!player || !opponent) {
    return null
  }

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl="" // Placeholder - should come from asset system
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl="" // Placeholder - should come from asset system
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="" // Placeholder - should come from asset system
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="" // Placeholder - should come from asset system
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-white p-4 border-t-2 border-gray-200">
        <div className="flex flex-wrap gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                type: skill.meta.skill_type
              }}
            >
              {skill.display_name}
            </SkillButton>
          ))}

          {/* Only render game control buttons if we have valid UIDs for them */}
          {availableButtonSlugs.includes('swap') && playerCreature && (
            <SkillButton
              uid={`${playerCreature.uid}-swap`}
              description="Switch to a different creature"
              stats={{
                type: "action"
              }}
            >
              <div className="flex items-center">
                <Shield className="mr-2" />
                Swap Creature
              </div>
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  )
}
