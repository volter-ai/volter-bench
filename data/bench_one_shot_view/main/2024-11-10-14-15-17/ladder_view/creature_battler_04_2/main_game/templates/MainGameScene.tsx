import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/CreatureCard"
import { SkillButton } from "@/components/ui/custom/SkillButton"

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
    creature_type: string
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

const getCreatureImageUrl = (type: string, isFront: boolean): string => {
  try {
    return `/creatures/${type}_${isFront ? 'front' : 'back'}.png`
  } catch {
    return '/creatures/fallback.png'
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature } = props.data?.entities || {}

  if (!player_creature || !opponent_creature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  const availableSkills = player_creature.collections?.skills?.filter(skill => 
    availableButtonSlugs?.includes(skill.uid)
  ) || []

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs?.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  return (
    <div className="w-full h-full aspect-video relative bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status (Top Left) */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={getCreatureImageUrl(opponent_creature.meta.creature_type, true)}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature (Top Right) */}
        <div className="flex justify-end items-start">
          <div className="relative">
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            <img
              src={getCreatureImageUrl(opponent_creature.meta.creature_type, true)}
              alt={opponent_creature.display_name}
              className="w-48 h-48 object-contain"
              onError={(e) => {
                e.currentTarget.src = '/creatures/fallback.png'
              }}
            />
          </div>
        </div>

        {/* Player Creature (Bottom Left) */}
        <div className="flex justify-start items-end">
          <div className="relative">
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            <img
              src={getCreatureImageUrl(player_creature.meta.creature_type, false)}
              alt={player_creature.display_name}
              className="w-48 h-48 object-contain"
              onError={(e) => {
                e.currentTarget.src = '/creatures/fallback.png'
              }}
            />
          </div>
        </div>

        {/* Player Status (Bottom Right) */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={getCreatureImageUrl(player_creature.meta.creature_type, false)}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-white/80">
        {availableSkills.length > 0 ? (
          availableSkills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              onClick={() => handleSkillClick(skill.uid)}
            />
          ))
        ) : (
          <div className="col-span-2 row-span-2 flex items-center justify-center text-gray-500">
            No available actions
          </div>
        )}
      </div>
    </div>
  )
}
