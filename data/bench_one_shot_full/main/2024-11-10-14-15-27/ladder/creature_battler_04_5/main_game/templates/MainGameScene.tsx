import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Sword } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  if (!playerCreature || !opponentCreature || !player || !opponent) {
    return null
  }

  return (
    <div className="w-full h-full aspect-video flex flex-col" uid="main-game-container">
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-gradient-to-b from-blue-100 to-green-100" uid="battlefield-container">
        {/* Top Left - Opponent Info */}
        <div className="flex items-start justify-start" uid="opponent-info">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/players/${opponent.meta?.prototype_id || 'default'}.png`}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center" uid="opponent-creature">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.meta?.prototype_id || 'default'}_front.png`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="transform scale-75"
          />
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center" uid="player-creature">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.meta?.prototype_id || 'default'}_back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            className="transform scale-75"
          />
        </div>

        {/* Bottom Right - Player Info */}
        <div className="flex items-end justify-end" uid="player-info">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta?.prototype_id || 'default'}.png`}
          />
        </div>
      </div>

      {/* Battle UI Area (lower 1/3) */}
      <div className="h-1/3 p-4 bg-white/90" uid="battle-ui">
        <div className="grid grid-cols-2 gap-4 h-full" uid="skills-grid">
          {playerCreature.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              variant="outline"
              className="h-full text-lg"
            />
          )) ?? (
            <div uid="no-skills-message" className="col-span-2 text-center text-gray-500">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
