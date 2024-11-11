import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
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
    [key: string]: any
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
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  meta: {
    prototype_id: string
  }
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

  const { player, bot, player_creature, bot_creature } = props.data.entities

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="h-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="h-screen w-full flex flex-col">
      {/* Top HUD */}
      <nav className="h-[10vh] bg-secondary flex items-center justify-between px-4">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl={`/players/${player.meta.prototype_id}.png`}
          className="w-[200px] h-[8vh]"
        />
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
          <span>VS</span>
          <Swords className="h-5 w-5" />
        </div>
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl={`/players/${bot.meta.prototype_id}.png`}
          className="w-[200px] h-[8vh]"
        />
      </nav>

      {/* Battlefield */}
      <div className="h-[50vh] flex items-center justify-between px-12 bg-background">
        <div className="relative">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.meta.prototype_id}.png`}
            className="transform hover:scale-105 transition-transform"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full text-sm">
            Player
          </div>
        </div>

        <div className="relative">
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            currentHp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl={`/creatures/${bot_creature.meta.prototype_id}.png`}
            className="transform hover:scale-105 transition-transform"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
        </div>
      </div>

      {/* Control Area */}
      <div className="h-[40vh] bg-secondary/50 rounded-t-xl p-6">
        <div className="grid grid-cols-2 gap-4 max-w-2xl mx-auto">
          {player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
