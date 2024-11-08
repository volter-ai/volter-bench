import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
}

interface Creature {
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
  uid: string
  display_name: string
}

interface GameUIData {
  entities: {
    player?: Player
    opponent?: Player
    player_creature?: Creature
    opponent_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature, player, opponent } = props.data?.entities || {}

  if (!player_creature || !opponent_creature || !player || !opponent) {
    return <div className="grid h-full w-full place-items-center bg-slate-900 text-white">
      Loading battle...
    </div>
  }

  const availableSkills = player_creature.collections?.skills?.filter(skill => 
    availableButtonSlugs?.includes(`skill_${skill.uid}`)
  ) || []

  return (
    <div className="flex flex-col h-full w-full bg-slate-900 text-white">
      {/* HUD */}
      <div className="bg-slate-800 p-4 flex justify-between items-center">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/assets/players/${player.uid}.png`}
          />
        )}
        <div className="flex gap-4">
          <Shield className="w-6 h-6" />
          <Swords className="w-6 h-6" />
        </div>
        {opponent && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/assets/players/${opponent.uid}.png`}
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-12">
        {player_creature && (
          <div className="relative">
            <span className="absolute -top-8 left-0 text-sm">Your Creature</span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats?.hp ?? 0}
              maxHp={player_creature.stats?.max_hp ?? 1}
              imageUrl={`/assets/creatures/${player_creature.uid}.png`}
            />
          </div>
        )}
        
        {opponent_creature && (
          <div className="relative">
            <span className="absolute -top-8 right-0 text-sm">Opponent's Creature</span>
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats?.hp ?? 0}
              maxHp={opponent_creature.stats?.max_hp ?? 1}
              imageUrl={`/assets/creatures/${opponent_creature.uid}.png`}
            />
          </div>
        )}
      </div>

      {/* UI Area */}
      <div className="min-h-[200px] bg-slate-700 p-4 rounded-t-lg">
        {availableSkills && availableSkills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 h-full">
            {availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats?.base_damage}
                onClick={() => emitButtonClick(`skill_${skill.uid}`)}
              />
            ))}
          </div>
        ) : (
          <div className="grid place-items-center h-full">
            <p>Waiting for available actions...</p>
          </div>
        )}
      </div>
    </div>
  )
}
