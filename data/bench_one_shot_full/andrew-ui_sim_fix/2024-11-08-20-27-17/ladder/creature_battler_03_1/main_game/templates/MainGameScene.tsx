import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
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
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
    attack: number
    defense: number
    speed: number
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

  const { player_creature, opponent_creature, player, opponent } = props.data.entities

  if (!player_creature || !opponent_creature || !player || !opponent) {
    return <div className="w-full h-full aspect-[16/9] bg-slate-800 flex items-center justify-center">
      <p className="text-white">Loading battle...</p>
    </div>
  }

  const availableSkills = player_creature.collections.skills?.filter(skill => 
    availableButtonSlugs.includes(skill.uid)
  ) || []

  return (
    <div className="w-full h-full aspect-[16/9] bg-slate-800 flex flex-col">
      {/* HUD */}
      <div className="w-full bg-slate-900 p-4 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl=""
        />
        <PlayerCard
          uid={opponent.uid}
          name={opponent.display_name}
          imageUrl=""
        />
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 bg-slate-700">
        <div className="flex flex-col items-center gap-2">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl=""
          />
          <div className="flex gap-2 text-white">
            <div className="flex items-center gap-1">
              <Sword className="w-4 h-4" />
              <span>{player_creature.stats.attack}</span>
            </div>
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4" />
              <span>{player_creature.stats.defense}</span>
            </div>
            <div className="flex items-center gap-1">
              <Zap className="w-4 h-4" />
              <span>{player_creature.stats.speed}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-center gap-2">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            imageUrl=""
          />
          <div className="flex gap-2 text-white">
            <div className="flex items-center gap-1">
              <Sword className="w-4 h-4" />
              <span>{opponent_creature.stats.attack}</span>
            </div>
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4" />
              <span>{opponent_creature.stats.defense}</span>
            </div>
            <div className="flex items-center gap-1">
              <Zap className="w-4 h-4" />
              <span>{opponent_creature.stats.speed}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Action UI */}
      <div className="bg-slate-900 p-4 min-h-[200px]">
        {availableButtonSlugs.length > 0 && availableSkills.length > 0 ? (
          <div className="grid grid-cols-2 gap-2">
            {availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-white">Waiting for available actions...</p>
          </div>
        )}
      </div>
    </div>
  )
}
