import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Droplet, Flame } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface ExamplePlayer {
    uid: string;
    stats: {
        stat1: number;
    };
}

interface Skill {
    uid: string;
    display_name: string;
    description: string;
    meta: {
        skill_type: string;
        prototype_id: string;
    };
    stats: {
        base_damage: number;
    };
}

interface Creature {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        hp: number;
        max_hp: number;
    };
    meta: {
        creature_type: string;
        prototype_id: string;
    };
    collections: {
        skills: Skill[];
    };
}

interface GameUIData {
    entities: {
        player: ExamplePlayer;
        opponent: ExamplePlayer;
        player_creature: Creature;
        opponent_creature: Creature;
    };
}

const CreatureStatus = ({ creature, uid }: { creature: Creature; uid: string }) => {
    const hpPercentage = creature?.stats ? (creature.stats.hp / creature.stats.max_hp) * 100 : 0;
    
    return (
        <Card className="p-4" key={uid}>
            <h3 className="font-bold">{creature?.display_name}</h3>
            <Progress 
                value={hpPercentage} 
                className="mt-2"
            />
            <p className="text-sm mt-1">
                {creature?.stats?.hp ?? 0} / {creature?.stats?.max_hp ?? 0} HP
            </p>
        </Card>
    );
};

const CreatureDisplay = ({ creature, isPlayer, uid }: { creature: Creature; isPlayer: boolean; uid: string }) => {
    const TypeIcon = creature?.meta?.creature_type === 'water' ? Droplet : Flame;
    
    return (
        <div className="relative flex flex-col items-center" key={uid}>
            <div className="w-32 h-32 bg-gray-800/10 rounded-full absolute bottom-0" />
            <div className="mb-4">
                <TypeIcon className={`w-16 h-16 ${isPlayer ? 'transform rotate-180' : ''}`} />
            </div>
        </div>
    );
};

export function MainGameSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    const playerCreature = props.data?.entities?.player_creature;
    const opponentCreature = props.data?.entities?.opponent_creature;

    if (!playerCreature || !opponentCreature) {
        return <div>Loading battle...</div>;
    }

    return (
        <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-blue-100 to-blue-200">
            {/* Battlefield Area (upper 2/3) */}
            <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
                {/* Opponent Status (Top Left) */}
                <div className="flex items-start justify-start">
                    <CreatureStatus 
                        creature={opponentCreature} 
                        uid={opponentCreature.uid} 
                    />
                </div>
                
                {/* Opponent Creature (Top Right) */}
                <div className="flex items-center justify-center">
                    <CreatureDisplay 
                        creature={opponentCreature} 
                        isPlayer={false} 
                        uid={opponentCreature.uid}
                    />
                </div>
                
                {/* Player Creature (Bottom Left) */}
                <div className="flex items-end justify-center">
                    <CreatureDisplay 
                        creature={playerCreature} 
                        isPlayer={true} 
                        uid={playerCreature.uid}
                    />
                </div>
                
                {/* Player Status (Bottom Right) */}
                <div className="flex items-end justify-end">
                    <CreatureStatus 
                        creature={playerCreature} 
                        uid={playerCreature.uid}
                    />
                </div>
            </div>

            {/* Battle Controls (lower 1/3) */}
            <Card className="h-1/3 p-4">
                <div className="grid grid-cols-2 gap-4 h-full">
                    {availableButtonSlugs?.map((buttonId) => (
                        <Button
                            key={buttonId}
                            onClick={() => emitButtonClick(buttonId)}
                            variant="default"
                            className="flex items-center justify-center gap-2"
                        >
                            <Sword className="w-5 h-5" />
                            {buttonId.charAt(0).toUpperCase() + buttonId.slice(1)}
                        </Button>
                    ))}
                </div>
            </Card>
        </div>
    );
}
