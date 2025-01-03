import { useCurrentButtons } from "@/lib/useChoices.ts"
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
    [key: string]: any
  }
}

interface Creature {
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
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
    player_creature: Creature
    bot_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  // Safely access entities with null checks
  const player = props.data?.entities?.player
  const bot = props.data?.entities?.bot
  const playerCreature = props.data?.entities?.player_creature
  const botCreature = props.data?.entities?.bot_creature

  // If critical data is missing, show error state
  if (!player || !bot || !playerCreature || !botCreature) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-slate-900 text-white">
        Error: Missing critical game data
      </div>
    )
  }

  return (
    <div className="h-screen w-full flex flex-col bg-slate-900">
      {/* HUD */}
      <nav className="h-[15%] bg-slate-800 p-4 flex justify-between items-center">
        {player && (
          <PlayerCard 
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/assets/players/${player.uid}.png`}
          />
        )}
        <div className="flex gap-4">
          <Shield className="w-6 h-6 text-blue-400" />
          <Swords className="w-6 h-6 text-red-400" />
        </div>
        {bot && (
          <PlayerCard 
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/assets/players/${bot.uid}.png`}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="h-[50%] flex justify-between items-center px-16">
        {playerCreature && (
          <div className="relative">
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/assets/creatures/${playerCreature.uid}.png`}
            />
            <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-blue-500 text-white px-3 py-1 rounded-full">
              Player
            </div>
          </div>
        )}

        {botCreature && (
          <div className="relative">
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl={`/assets/creatures/${botCreature.uid}.png`}
            />
            <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-red-500 text-white px-3 py-1 rounded-full">
              Opponent
            </div>
          </div>
        )}
      </div>

      {/* UI Area */}
      <div className="h-[35%] bg-slate-700 p-4 flex flex-col gap-4">
        <div className="flex flex-wrap gap-4 justify-center">
          {playerCreature?.collections?.skills?.length > 0 ? (
            playerCreature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage,
                  ...skill.stats
                }}
              />
            ))
          ) : (
            <div className="text-white text-center">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
