import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
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

const DEFAULT_CREATURE_IMAGE = "/images/default-creature.png"
const DEFAULT_PLAYER_IMAGE = "/images/default-player.png"

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const botCreature = props.data?.entities?.bot_creature
  const player = props.data?.entities?.player
  const bot = props.data?.entities?.bot

  if (!playerCreature || !botCreature || !player || !bot) {
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading game data...
    </div>
  }

  return (
    <div className="h-screen w-screen aspect-video bg-background flex flex-col">
      {/* HUD */}
      <nav className="w-full h-16 bg-muted flex justify-between items-center px-4">
        {player && (
          <PlayerCard 
            uid={player.uid}
            name={player.display_name}
            imageUrl={DEFAULT_PLAYER_IMAGE}
          />
        )}
        
        <div className="flex gap-4">
          <Shield className="w-6 h-6" />
          <Swords className="w-6 h-6" />
        </div>

        {bot && (
          <PlayerCard 
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={DEFAULT_PLAYER_IMAGE}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-20">
        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Your Creature
          </span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats?.hp ?? 0}
            maxHp={playerCreature.stats?.max_hp ?? 0}
            imageUrl={DEFAULT_CREATURE_IMAGE}
          />
        </div>
        
        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Opponent's Creature
          </span>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            currentHp={botCreature.stats?.hp ?? 0}
            maxHp={botCreature.stats?.max_hp ?? 0}
            imageUrl={DEFAULT_CREATURE_IMAGE}
          />
        </div>
      </div>

      {/* Control Area */}
      <div className="h-48 bg-muted p-4 flex flex-wrap gap-2 content-start">
        {playerCreature.collections?.skills?.length > 0 ? (
          playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats?.base_damage
              }}
            />
          ))
        ) : (
          <div className="w-full h-full flex items-center justify-center text-muted-foreground">
            No skills available
          </div>
        )}
      </div>
    </div>
  )
}
