import { useCurrentButtons } from "@/lib/useChoices.ts"
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, bot, player_creature, bot_creature } = props.data?.entities || {}

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="h-screen aspect-video bg-background flex items-center justify-center">
      Loading game data...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    const matchingSlug = availableButtonSlugs.find(slug => 
      slug.toLowerCase().includes(skillUid.toLowerCase())
    )
    
    if (matchingSlug) {
      emitButtonClick(matchingSlug)
    }
  }

  const skills = player_creature.collections?.skills || []

  return (
    <div className="h-screen aspect-video bg-background flex flex-col">
      {/* HUD */}
      <div className="h-1/6 flex justify-between items-center px-4 border-b">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl=""
        />
        <div className="flex gap-4">
          <Shield className="w-6 h-6" />
          <Swords className="w-6 h-6" />
        </div>
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl=""
        />
      </div>

      {/* Battlefield */}
      <div className="h-3/6 flex justify-between items-center px-16">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl=""
          />
          <div className="mt-2 text-sm font-bold">Your Creature</div>
        </div>

        <div className="flex flex-col items-center">
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            currentHp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl=""
          />
          <div className="mt-2 text-sm font-bold">Opponent's Creature</div>
        </div>
      </div>

      {/* UI Area */}
      <div className="h-2/6 bg-muted p-4 rounded-t-lg">
        <div className="grid grid-cols-2 gap-4 h-full">
          {skills.length > 0 ? (
            skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
                disabled={!availableButtonSlugs.some(slug => 
                  slug.toLowerCase().includes(skill.uid.toLowerCase())
                )}
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))
          ) : (
            <div className="col-span-2 text-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
