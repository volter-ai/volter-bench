import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
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

  if (!player || !opponent) return null

  return (
    <div className="w-full h-full aspect-video bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
        {/* Top left - Opponent Status */}
        <div className="flex items-start justify-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl={`/players/${opponent.uid}/avatar.png`}
            />
          )}
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.uid}/front.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top right - Opponent Creature */}
        <div className="flex items-center justify-center">
          {opponentCreature && (
            <div className="relative">
              <img 
                src={`/creatures/${opponentCreature.uid}/front.png`}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
              <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            </div>
          )}
        </div>

        {/* Bottom left - Player Creature */}
        <div className="flex items-center justify-center">
          {playerCreature && (
            <div className="relative">
              <img 
                src={`/creatures/${playerCreature.uid}/back.png`}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
              <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            </div>
          )}
        </div>

        {/* Bottom right - Player Status */}
        <div className="flex items-end justify-end flex-col gap-4">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/players/${player.uid}/avatar.png`}
            />
          )}
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.uid}/back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-white/90 p-4 flex flex-col gap-2">
        <div className="flex gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            skill && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                description={skill.description}
                stats={{ damage: skill.stats.base_damage }}
              >
                <Sword className="mr-2 h-4 w-4" />
                {skill.display_name}
              </SkillButton>
            )
          ))}
        </div>

        <div className="flex gap-2 justify-center">
          {/* Only show these buttons if they're available and we have valid entities to reference */}
          {availableButtonSlugs.includes('swap') && player && (
            player.entities.active_creature && (
              <SkillButton
                uid={`${player.entities.active_creature.uid}_swap`}
                description="Switch to another creature"
                stats={{}}
              >
                <SwapHorizontal className="mr-2 h-4 w-4" />
                Swap
              </SkillButton>
            )
          )}

          {availableButtonSlugs.includes('back') && player && (
            player.entities.active_creature && (
              <SkillButton
                uid={`${player.entities.active_creature.uid}_back`}
                description="Go back"
                stats={{}}
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back
              </SkillButton>
            )
          )}
        </div>
      </div>
    </div>
  )
}
