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
  const player = props.data?.entities?.player
  
  if (!playerCreature || playerCreature.__type !== "Creature" ||
      !botCreature || botCreature.__type !== "Creature" ||
      !player || player.__type !== "Player") {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading game data...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  const skills = playerCreature.collections?.skills?.filter(skill => 
    skill && skill.__type === "Skill"
  ) || []

  return (
    <div className="h-screen w-full flex flex-col" role="application" aria-label="Game Scene">
      <nav className="h-16 bg-primary/10 flex items-center justify-between px-4">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl="/player.png"
        />
        <div className="flex items-center gap-4">
          <Sword className="w-6 h-6" />
          <Shield className="w-6 h-6" />
        </div>
      </nav>

      <main className="flex-1 flex items-center justify-between px-8">
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Your Creature</span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl="/creature.png"
          />
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Opponent's Creature</span>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            hp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl="/creature.png"
          />
        </div>
      </main>

      <section 
        className="min-h-[200px] max-h-[33vh] bg-secondary/10 p-4 overflow-y-auto"
        role="region" 
        aria-label="Skills"
      >
        <div className="flex flex-wrap gap-4 justify-center">
          {skills.length > 0 ? (
            skills.map((skill) => (
              <div key={skill.uid} className="skill-button-wrapper">
                <SkillButton
                  uid={skill.uid}
                  name={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  disabled={!availableButtonSlugs.includes(skill.uid)}
                  onClick={() => handleSkillClick(skill.uid)}
                />
              </div>
            ))
          ) : (
            <div role="alert">No skills available</div>
          )}
        </div>
      </section>
    </div>
  )
}
