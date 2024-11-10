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

  // Safety checks
  if (!props.data?.entities) {
    return <div className="h-screen w-screen flex items-center justify-center">Loading game data...</div>
  }

  const { player, bot, player_creature, bot_creature } = props.data.entities

  // Verify all required entities exist and are of correct type
  if (player?.__type !== "Player" || bot?.__type !== "Player" || 
      player_creature?.__type !== "Creature" || bot_creature?.__type !== "Creature") {
    return <div className="h-screen w-screen flex items-center justify-center">Invalid game state</div>
  }

  // Helper function to check if a skill button is available
  const isSkillAvailable = (skillUid: string) => {
    return availableButtonSlugs.includes(`skill_${skillUid}`)
  }

  // Handle skill button click
  const handleSkillClick = (skillUid: string) => {
    const buttonSlug = `skill_${skillUid}`
    if (isSkillAvailable(skillUid)) {
      emitButtonClick(buttonSlug)
    }
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-[10%] bg-secondary p-4 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl="/players/default.png"
        />
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl="/players/default.png"
        />
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] relative flex justify-between items-center px-16">
        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-4 py-1 rounded-full">
            Player
          </div>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.meta?.prototype_id || 'default'}.png`}
          />
        </div>

        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-4 py-1 rounded-full">
            Opponent
          </div>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            currentHp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl={`/creatures/${bot_creature.meta?.prototype_id || 'default'}.png`}
          />
        </div>
      </div>

      {/* Control Area */}
      <div className="h-[30%] bg-card rounded-t-xl p-6 shadow-lg">
        <div className="grid grid-cols-2 gap-4 h-full">
          {player_creature.collections.skills && player_creature.collections.skills.length > 0 ? (
            player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
                onClick={() => handleSkillClick(skill.uid)}
                disabled={!isSkillAvailable(skill.uid)}
              />
            ))
          ) : (
            <div className="col-span-2 flex items-center justify-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
