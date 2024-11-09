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
  meta: {
    prototype_id: string
    category: string
    skill_type: string
    is_physical: boolean
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
    sp_attack: number
    sp_defense: number
    speed: number
  }
  meta: {
    prototype_id: string
    category: string
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
  description: string
  meta: {
    prototype_id: string
    category: string
  }
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
    availableButtonSlugs = [],
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const opponentCreature = props.data?.entities?.opponent_creature
  const player = props.data?.entities?.player
  const opponent = props.data?.entities?.opponent

  if (!playerCreature || !opponentCreature || !player || !opponent) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading...
    </div>
  }

  const availableSkills = playerCreature.collections?.skills?.filter(skill => 
    availableButtonSlugs.includes(`skill_${skill.uid}`)
  ) || []

  const defaultActions = [
    { uid: 'run', display_name: 'Run', description: 'Flee from battle' },
    { uid: 'switch', display_name: 'Switch', description: 'Switch creature' }
  ].filter(action => availableButtonSlugs.includes(action.uid))

  const actions = [...availableSkills, ...defaultActions]

  return (
    <div className="w-full h-full flex flex-col bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex items-center justify-start pl-8">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/players/${opponent.meta.prototype_id}.png`}
            className="transform scale-75"
          />
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
            className="transform scale-75 -ml-4"
          />
        </div>
        
        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm"></div>
            <img 
              src={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain relative z-10"
            />
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm"></div>
            <img 
              src={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain relative z-10"
            />
          </div>
        </div>

        {/* Player Status */}
        <div className="flex items-center justify-end pr-8">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
            className="transform scale-75 mr-4"
          />
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta.prototype_id}.png`}
            className="transform scale-75"
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white/90 rounded-t-xl p-4 relative z-20">
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
          {actions.length > 0 ? (
            actions.map((action) => {
              const buttonSlug = 'stats' in action ? `skill_${action.uid}` : action.uid
              return (
                <SkillButton
                  key={action.uid}
                  uid={action.uid}
                  skillName={action.display_name}
                  description={action.description}
                  damage={('stats' in action) ? action.stats.base_damage : undefined}
                  type={('meta' in action) ? action.meta.skill_type : undefined}
                  className="w-full h-full"
                  onClick={() => {
                    if (availableButtonSlugs.includes(buttonSlug)) {
                      emitButtonClick(buttonSlug)
                    }
                  }}
                />
              )
            })
          ) : (
            <div className="col-span-2 flex items-center justify-center text-gray-500">
              Waiting for available actions...
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
