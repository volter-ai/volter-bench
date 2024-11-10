import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Creature {
    uid: string;
    display_name: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        speed: number;
    };
    collections: {
        skills: Skill[];
    };
}

interface Skill {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
    };
}

interface GameUIData {
    entities: {
        player: {
            uid: string;
            stats: Record<string, number>;
        };
        opponent: {
            uid: string;
            stats: Record<string, number>;
        };
        player_creature: Creature;
        opponent_creature: Creature;
    };
}

export function MainGameSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    const playerCreature = props.data.entities.player_creature;
    const opponentCreature = props.data.entities.opponent_creature;

    if (!playerCreature || !opponentCreature) return null;

    const CreatureCard = ({ creature, isPlayer }: { creature: Creature, isPlayer: boolean }) => (
        <Card className={`relative p-4 ${isPlayer ? 'ml-4' : 'mr-4'}`}>
            <div className="text-lg font-bold mb-2">{creature.display_name}</div>
            
            <div className="mb-4">
                <div className="text-sm text-muted-foreground mb-1">
                    HP: {creature.stats.hp}/{creature.stats.max_hp}
                </div>
                <div className="w-full h-2 bg-secondary rounded-full">
                    <div 
                        className="h-full bg-primary rounded-full transition-all duration-300"
                        style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
                    />
                </div>
            </div>

            <div className="flex gap-2 text-sm text-muted-foreground">
                <div className="flex items-center">
                    <Sword className="w-4 h-4 mr-1" /> {creature.stats.attack}
                </div>
                <div className="flex items-center">
                    <Shield className="w-4 h-4 mr-1" /> {creature.stats.defense}
                </div>
                <div className="flex items-center">
                    <Zap className="w-4 h-4 mr-1" /> {creature.stats.speed}
                </div>
            </div>
        </Card>
    );

    return (
        <div className="h-full w-full flex flex-col">
            {/* HUD */}
            <div className="h-[10%] bg-secondary px-4 flex items-center">
                <h1 className="text-xl font-bold">Battle Arena</h1>
            </div>

            {/* Battlefield */}
            <div className="h-[50%] flex items-center justify-between px-8">
                <div className="text-center">
                    <div className="text-sm text-muted-foreground mb-2">Player</div>
                    <CreatureCard creature={playerCreature} isPlayer={true} />
                </div>
                <div className="text-center">
                    <div className="text-sm text-muted-foreground mb-2">Opponent</div>
                    <CreatureCard creature={opponentCreature} isPlayer={false} />
                </div>
            </div>

            {/* UI Region */}
            <Card className="h-[40%] p-4 rounded-t-xl">
                <div className="grid grid-cols-2 gap-4">
                    {playerCreature.collections.skills?.map((skill) => {
                        const skillId = skill.meta.prototype_id;
                        return availableButtonSlugs.includes(skillId) && (
                            <Button
                                key={skill.uid}
                                onClick={() => emitButtonClick(skillId)}
                                variant="secondary"
                                className="h-auto flex flex-col items-start p-4"
                            >
                                <div className="font-bold">{skill.display_name}</div>
                                <div className="text-sm text-muted-foreground">{skill.description}</div>
                                <div className="text-sm text-muted-foreground mt-2">
                                    Damage: {skill.stats.base_damage}
                                </div>
                            </Button>
                        );
                    })}
                </div>
            </Card>
        </div>
    );
}
