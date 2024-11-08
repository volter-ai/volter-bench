import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    damage: number
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
    skills?: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures?: Creature[]
  }
}

interface GameUIData {
  entities: {
    player?: Player
    bot?: Player
    player_creature?: Creature
    bot_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, bot, player_creature, bot_creature } = props.data.entities

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="h-screen w-full flex flex-col bg-background">
      {/* HUD */}
      <nav className="w-full p-4 bg-primary/10 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.display_name.toLowerCase()}.png`}
          />
          <Sword className="h-5 w-5" />
        </div>
        <div className="flex items-center gap-4">
          <Shield className="h-5 w-5" />
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/${bot.display_name.toLowerCase()}.png`}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 grid grid-cols-2 gap-8 p-8">
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Your Creature</span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.display_name.toLowerCase()}.png`}
          />
        </div>
        
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Opponent's Creature</span>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl={`/creatures/${bot_creature.display_name.toLowerCase()}.png`}
          />
        </div>
      </div>

      {/* Skills UI */}
      <div className="p-8 bg-secondary/10">
        <div className="flex flex-wrap gap-4 justify-center">
          {player_creature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          )) ?? <div>No skills available</div>}
        </div>
      </div>
    </div>
  )
}
