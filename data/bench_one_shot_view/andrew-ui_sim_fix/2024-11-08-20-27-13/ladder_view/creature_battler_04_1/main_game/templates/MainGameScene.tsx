import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
    creature_type: string
  }
  collections?: {
    skills?: Skill[]
  }
}

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

interface Player {
  __type: "Player"
  uid: string
  display_name: string
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
    player_creature?: Creature
    opponent_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, opponent, player_creature, opponent_creature } = props.data.entities

  if (!player_creature || !opponent_creature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  return (
    <div className="relative w-full h-full flex flex-col overflow-hidden">
      {/* Battlefield Area */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4 bg-gradient-to-b from-sky-900/20 to-sky-800/20">
        {/* Opponent Status (Top Left) */}
        <div className="flex flex-col gap-2 items-start justify-start">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl="/players/opponent.png"
            className="w-full max-w-[250px]"
          />
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/creatures/${opponent_creature.meta.creature_type}.png`}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            className="w-full max-w-[250px]"
          />
        </div>

        {/* Opponent Creature (Top Right) */}
        <div className="flex items-center justify-center">
          <div className="relative w-40 h-40">
            <img 
              src={`/creatures/${opponent_creature.meta.creature_type}_front.png`}
              alt={opponent_creature.display_name}
              className="w-full h-full object-contain"
              onError={(e) => {
                e.currentTarget.src = "/creatures/fallback.png"
              }}
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm transform translate-y-2" />
          </div>
        </div>

        {/* Player Creature (Bottom Left) */}
        <div className="flex items-center justify-center">
          <div className="relative w-40 h-40">
            <img 
              src={`/creatures/${player_creature.meta.creature_type}_back.png`}
              alt={player_creature.display_name}
              className="w-full h-full object-contain"
              onError={(e) => {
                e.currentTarget.src = "/creatures/fallback.png"
              }}
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm transform translate-y-2" />
          </div>
        </div>

        {/* Player Status (Bottom Right) */}
        <div className="flex flex-col gap-2 items-end justify-end">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/players/player.png"
            className="w-full max-w-[250px]"
          />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/creatures/${player_creature.meta.creature_type}.png`}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            className="w-full max-w-[250px]"
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 min-h-[200px] grid grid-cols-2 gap-4 p-4 bg-gray-900/20">
        {(player_creature.collections?.skills?.length ?? 0) > 0 ? (
          player_creature.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              className="w-full h-full max-h-24"
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => handleSkillClick(skill.uid)}
            />
          ))
        ) : (
          <div className="col-span-2 flex items-center justify-center text-gray-400">
            No skills available
          </div>
        )}
      </div>
    </div>
  )
}
