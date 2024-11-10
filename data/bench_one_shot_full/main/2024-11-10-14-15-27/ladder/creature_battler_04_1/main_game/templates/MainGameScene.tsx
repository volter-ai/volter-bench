import { useCurrentButtons } from "@/lib/useChoices.ts"
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
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
  meta: {
    prototype_id: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
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

  const playerCreature = props.data.entities?.player_creature
  const opponentCreature = props.data.entities?.opponent_creature
  const player = props.data.entities?.player
  const opponent = props.data.entities?.opponent

  if (!playerCreature || !opponentCreature || !player || !opponent) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  // Helper to get creature image URL based on prototype_id
  const getCreatureImageUrl = (creature: Creature, view: 'front' | 'back') => 
    `/assets/creatures/${creature.meta.prototype_id}/${view}.png`

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={getCreatureImageUrl(opponentCreature, 'front')}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-start justify-end">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={getCreatureImageUrl(opponentCreature, 'front')}
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-start">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={getCreatureImageUrl(playerCreature, 'back')}
          />
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={getCreatureImageUrl(playerCreature, 'front')}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 p-4">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections?.skills?.slice(0, 4).map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              variant="secondary"
              className="h-24"
            />
          ))}
        </div>
      </div>
    </div>
  )
}
