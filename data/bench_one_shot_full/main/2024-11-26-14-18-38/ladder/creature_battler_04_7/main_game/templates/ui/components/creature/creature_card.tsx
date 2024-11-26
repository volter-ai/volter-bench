import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col items-center gap-4">
            <img 
              src={image} 
              alt={name}
              className="w-32 h-32 object-contain"
            />
            <div className="w-full bg-secondary rounded-full h-2.5">
              <div 
                className="bg-primary h-2.5 rounded-full" 
                style={{width: `${(currentHp/maxHp) * 100}%`}}
              />
            </div>
            <span className="text-sm">
              {currentHp} / {maxHp} HP
            </span>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
