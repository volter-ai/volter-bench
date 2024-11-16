import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface BaseProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

interface CreatureCardProps extends BaseProps {
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CustomCard = React.forwardRef<HTMLDivElement, BaseProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, BaseProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, BaseProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, BaseProps>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CustomProgress = React.forwardRef<HTMLDivElement, BaseProps & { value: number }>(
  ({ uid, ...props }, ref) => <Progress ref={ref} {...props} />
)

CustomCard = withClickable(CustomCard)
CustomCardContent = withClickable(CustomCardContent)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardTitle = withClickable(CustomCardTitle)
CustomProgress = withClickable(CustomProgress)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <CustomCard uid={`${uid}-card`} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`}>
          <img
            src={image}
            alt={name}
            className="w-full h-48 object-contain mb-4"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{`${currentHp}/${maxHp}`}</span>
            </div>
            <CustomProgress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
