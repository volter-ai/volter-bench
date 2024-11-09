import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Activity } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
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

  // Safely destructure with null checks
  const { entities } = props.data || {}
  const { player_creature, opponent_creature } = entities || {}

  if (!player_creature || !opponent_creature) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-slate-900 text-white">
        Loading battle...
      </div>
    )
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-900">
      {/* HUD */}
      <nav className="h-[10%] min-h-[60px] bg-slate-800 flex items-center justify-between px-6 border-b border-slate-700">
        <div className="flex items-center gap-4">
          <Shield className="text-blue-400" />
          <span className="text-white">DEF: {player_creature.stats.defense}</span>
        </div>
        <div className="flex items-center gap-4">
          <Sword className="text-red-400" />
          <span className="text-white">ATK: {player_creature.stats.attack}</span>
        </div>
        <div className="flex items-center gap-4">
          <Activity className="text-green-400" />
          <span className="text-white">SPD: {player_creature.stats.speed}</span>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] flex justify-between items-center px-12 relative">
        {/* Player Creature */}
        <div className="flex-1 flex justify-start items-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.uid}.png`}
            className="transform translate-x-12 hover:scale-105 transition-transform"
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex-1 flex justify-end items-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            imageUrl={`/creatures/${opponent_creature.uid}.png`}
            className="transform -translate-x-12 hover:scale-105 transition-transform"
          />
        </div>
      </div>

      {/* Skills/Controls Area */}
      <div className="h-[30%] min-h-[200px] bg-slate-800 p-6 border-t border-slate-700">
        <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
          {player_creature.collections.skills?.length > 0 ? (
            player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                className="w-full h-full min-h-[48px]"
              />
            ))
          ) : (
            <div className="col-span-2 text-center text-white">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
