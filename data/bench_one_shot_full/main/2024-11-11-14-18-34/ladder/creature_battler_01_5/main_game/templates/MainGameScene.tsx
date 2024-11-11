import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
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

  const playerCreature = props.data?.entities?.player_creature
  const botCreature = props.data?.entities?.bot_creature

  if (!playerCreature || !botCreature) {
    return <div className="h-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    if (!skillUid || !availableButtonSlugs) return
    
    // Ensure we have a valid array of button slugs
    const buttonSlugs = Array.isArray(availableButtonSlugs) ? availableButtonSlugs : []
    
    // Only emit if the skill is available
    if (buttonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  // Ensure skills is always an array
  const skills = Array.isArray(playerCreature.collections?.skills) 
    ? playerCreature.collections.skills 
    : []

  return (
    <div className="h-screen w-full flex flex-col">
      {/* HUD */}
      <nav className="h-16 bg-primary flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6" />
          <span>Battle Arena</span>
        </div>
        <Swords className="h-6 w-6" />
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center px-8 bg-background">
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Player</span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.display_name.toLowerCase()}.png`}
          />
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Opponent</span>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            hp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={`/creatures/${botCreature.display_name.toLowerCase()}.png`}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/4 bg-secondary p-4">
        <div className="flex flex-wrap gap-4 justify-center">
          {skills.map((skill: Skill) => {
            if (!skill?.uid) return null;
            
            const buttonSlugs = Array.isArray(availableButtonSlugs) ? availableButtonSlugs : []
            const isAvailable = buttonSlugs.includes(skill.uid)
            
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name || 'Unknown Skill'}
                description={skill.description || 'No description available'}
                stats={`Damage: ${skill.stats?.damage ?? 0}`}
                disabled={!isAvailable}
                onClick={() => handleSkillClick(skill.uid)}
              />
            );
          })}
        </div>
      </div>
    </div>
  )
}
